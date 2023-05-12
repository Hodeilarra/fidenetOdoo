# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, date


class InvoiceFromPickingMass(models.Model):
    _name = 'invoice.from.picking.mass'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Invoice From Picking'
    _order = "id desc"

    @api.depends('invoice_ids')
    def _compute_count_invoices(self):
        in_invoices = self.invoice_ids.filtered(lambda s: s.invoicefrompicking_id.id == self.id and s.move_type == 'in_invoice')
        out_invoices = self.invoice_ids.filtered(lambda s: s.invoicefrompicking_id.id == self.id and s.move_type == 'out_invoice')
        self.count_in_invoices = len(in_invoices)
        self.count_out_invoices = len(out_invoices)

    name = fields.Char('Referencia', copy=False, default="Nuevo")
    invoicefrompicking_line_ids = fields.One2many('invoice.from.picking.mass.line', 'invoicefrompicking_id', copy=False,
                                                string='Albaranes')
    state = fields.Selection(string='Estado', selection=[('draft', 'Borrador'), ('process', 'Facturas Generadas'),
                                                         ('approved', 'Facturas Aprobadas')], default='draft')
    count_out_invoices = fields.Integer('Nº Facturas', compute='_compute_count_invoices')
    invoice_ids = fields.One2many('account.move', 'invoicefrompicking_id', 'Facturas')
    count_in_invoices = fields.Integer('Nº Facturas', compute='_compute_count_invoices')
    company_id = fields.Many2one(comodel_name="res.company", string="Compañía", default=lambda self: self.env.company,
                                 required=True)
    user_id = fields.Many2one('res.users', string="Creado por", default=lambda self: self.env.user)
    date_to_invoice = fields.Datetime(string='Fecha Facturas', default=fields.Datetime.now)
    type = fields.Selection(string='Tipo', selection=[('purchase', 'Compras'), ('sale', 'Ventas')])

    def action_view_out_invoices(self):
        invoices = []
        for inv in self.invoice_ids:
            if inv.move_type == 'out_invoice':
                invoices.append(inv.id)
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 0:
            action['domain'] = [('id', 'in', invoices)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def action_view_in_invoices(self):
        invoices = []
        for inv in self.invoice_ids:
            if inv.type == 'in_invoice':
                invoices.append(inv.id)
        action = self.env.ref('account.action_move_in_invoice_type').read()[0]
        if len(invoices) > 0:
            action['domain'] = [('id', 'in', invoices)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def _prepare_invoice_values(self, result, line, partner, type):
        if partner.parent_id:
            partner = partner.parent_id
        flag = True
        if result:
            for r in result:
                if r['partner_id'] == partner.id:
                    picking_id_name = ""
                    for l in line.picking_id.move_ids_without_package:
                        if picking_id_name != line.picking_id.name:
                            r['invoice_line_ids'].append({
                                'name': "Albarán:" + line.picking_id.name + ", Fecha: " + str(line.picking_id.date_done),
                                'display_type': 'line_section',
                            })
                        picking_id_name = line.picking_id.name

                        r['invoice_line_ids'].append({
                            'picking_id': line.picking_id.id,
                            'line_picking_id': l.id,
                            'sale_line_ids': l.sale_line_id.ids if l.sale_line_id else False,
                            'purchase_line_id': l.purchase_line_id.ids if l.purchase_line_id else False,
                            'product_id': l.product_id.id,
                            'quantity': l.quantity_done,
                            'price_unit': l.sale_line_id.price_unit if l.sale_line_id else l.purchase_line_id.price_unit,
                            'tax_ids': l.sale_line_id.tax_id.ids if l.sale_line_id else l.purchase_line_id.taxes_id.ids,
                            'discount': l.sale_line_id.discount if l.sale_line_id else 0.0,
                        })
                    flag = False
                    break

        if flag:
            invoice_lines = []
            for xline in line.picking_id:
                print(xline.name)
                """if picking_name != line.picking_id.name:"""
                line_vals = {
                    'name': "Albarán:" + xline.name + ", Fecha: " + str(line.picking_id.date_done),
                    'display_type': 'line_section',
                }
                invoice_lines.append((0, 0, line_vals))

                for l in xline.move_ids_without_package:
                    line_vals = {
                        'picking_id': line.picking_id.id,
                        'line_picking_id': l.id,
                        'sale_line_ids': l.sale_line_id.ids if l.sale_line_id else False,
                        'purchase_line_id': l.purchase_line_id.ids if l.purchase_line_id else False,
                        'product_id': l.product_id.id,
                        'quantity': l.quantity_done,
                        'price_unit': l.sale_line_id.price_unit if l.sale_line_id else l.purchase_line_id.price_unit,
                        'tax_ids': l.sale_line_id.tax_id.ids if l.sale_line_id else l.purchase_line_id.taxes_id.ids,
                        'discount': l.sale_line_id.discount if l.sale_line_id else 0.0,
                    }
                    print(line_vals)
                    invoice_lines.append((0, 0, line_vals))

            result.append({
                'ref': line.picking_id.sale_id.client_order_ref,
                'move_type': 'out_invoice' if type == 'sale' else 'in_invoice',
                'invoice_date': self.date_to_invoice,
                'invoice_origin': self.name,
                'picking_id': line.picking_id.id,
                'invoice_user_id': line.picking_id.sale_id.user_id.id if line.picking_id.sale_id else line.picking_id.purchase_id.user_id.id,
                'narration': line.picking_id.sale_id.note if line.picking_id.sale_id else line.picking_id.purchase_id.notes,
                'partner_id': partner.id,
                'fiscal_position_id': line.picking_id.partner_id.property_account_position_id.id,
                'partner_shipping_id': line.picking_id.sale_id.partner_shipping_id.id if line.picking_id.sale_id else False,
                'currency_id': line.picking_id.company_id.currency_id.id,
                'invoicefrompicking_id': self.id,
                'invoice_line_ids': invoice_lines,
            })

            print("----------------")
            print(invoice_lines)
            print("----------------")

        return result

    def make_invoice_picking(self):
        move_obj = self.env['account.move']
        for record in self:
            result = []
            billable = record.invoicefrompicking_line_ids.filtered(lambda s: s.picking_id.state_invoice == 'invoiced')
            if record.invoicefrompicking_line_ids:
                if not billable:
                    partners = record.invoicefrompicking_line_ids.mapped('partner_id')
                    for partner in partners:
                        for line in record.invoicefrompicking_line_ids.filtered(lambda s: s.partner_id.id == partner.id):
                            if line.picking_id.state_invoice == 'to_invoice':
                                result = (record._prepare_invoice_values(result, line, line.partner_id, record.type))
                    for r in result:
                        new_invoice = move_obj.create(r)
                        new_invoice._onchange_partner_id()
                    for l in record.invoicefrompicking_line_ids:
                        l.picking_id.state_invoice = 'invoiced'
                    record.update({
                        'state': 'process'
                    })
                else:
                    raise UserError('Hay albaranes que ya estan facturados, por favor realice la busqueda nuevamente')
            else:
                raise UserError('Debe generar una busqueda antes de facturar')

    def convert_to_draft(self):
        for record in self:
            for line in record.invoicefrompicking_line_ids:
                if line.picking_id.state_invoice == 'invoiced':
                    line.picking_id.state_invoice = 'to_invoice'
            for invoice in record.invoice_ids:
                invoice.unlink()
            record.update({
                'state': 'draft'
            })

    def approve_invoice_picking(self):
        for record in self:
            for invoice in record.invoice_ids:
                invoice.action_post()
                for line_invoice in invoice.invoice_line_ids:
                    if record.type == 'sale':
                        line_invoice.line_picking_id.sale_line_id.qty_invoiced = line_invoice.quantity
                    if record.type == 'purchase':
                        line_invoice.line_picking_id.purchase_line_id.qty_invoiced = line_invoice.quantity
            record.update({
                'state': 'approved'
            })

    @api.model
    def create(self, values):
        type_ifpm = values.get('type')
        if values.get('name', "Nuevo") == "Nuevo":
            if type_ifpm == 'sale':
                values['name'] = self.env['ir.sequence'].next_by_code('out.invoice.from.picking.mass') or "Nuevo"
            else:
                values['name'] = self.env['ir.sequence'].next_by_code('in.invoice.from.picking.mass') or "Nuevo"
        return super(InvoiceFromPickingMass, self).create(values)

class InvoiceFromPickingMassLine(models.Model):
    _name = 'invoice.from.picking.mass.line'
    _description = 'Invoice From Picking Line'

    picking_id = fields.Many2one('stock.picking', 'Nro. Doc.')
    partner_id = fields.Many2one('res.partner', 'Nombre R. Social')
    date = fields.Datetime(string='Fecha Pevista')
    origin = fields.Char('Su referencia')
    invoicefrompicking_id = fields.Many2one('invoice.from.picking.mass', 'Busqueda')

    @api.onchange('picking_id')
    def _onchange_picking_id(self):
        for line in self:
            if line.picking_id:
                picking = line.picking_id
                line.partner_id = picking.partner_id.id
                line.date = picking.scheduled_date
                line.origin = picking.sale_id.client_order_ref
