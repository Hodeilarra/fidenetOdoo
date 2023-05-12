# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class InvoiceFromPickingMassWzd(models.TransientModel):
    _name = 'invoice.from.picking.mass.wzd'
    _description = 'Wizard Invoice From Picking'

    @api.model
    def default_get(self, fields_list):
        res = super(InvoiceFromPickingMassWzd, self).default_get(fields_list)
        picking_obj = self.env['stock.picking']
        pickings = self._context.get('active_ids', [('state', '=', 'done')])
        results = []
        for id in pickings:
            picking = picking_obj.search([('id', '=', id)])
            if picking.state == 'done':
                results.append(id)
        res.update({
            'picking_ids': results
        })
        return res

    picking_ids = fields.Many2many('stock.picking', string='Pickings')

    def action_create_ifpm(self):
        ifpm_obj = self.env['invoice.from.picking.mass']
        lines = []
        for picking in self.picking_ids:
            if picking.state != 'done':
                raise UserError(_('The picking is not Done %s') % (picking.name))

        for picking in self.picking_ids.filtered(lambda s: s.picking_type_id.code == 'incoming'):
            line = {
                'picking_id': picking.id,
                'partner_id': picking.partner_id.parent_id.id if picking.partner_id.parent_id else picking.partner_id.id,
                'date': picking.scheduled_date,
                'origin': picking.origin,
            }
            lines.append([0, 0, line])
        vals = {
            'type': 'purchase',
            'date_to_invoice': fields.datetime.today(),
            'invoicefrompicking_line_ids': lines
        }
        purchase_ifpm = ifpm_obj.create(vals)
        lines = []
        for picking in self.picking_ids.filtered(lambda s: s.picking_type_id.code == 'outgoing'):
            line = {
                'picking_id': picking.id,
                'partner_id': picking.partner_id.parent_id.id if picking.partner_id.parent_id else picking.partner_id.id,
                'date': picking.scheduled_date,
                'origin': picking.origin,
            }
            lines.append([0, 0, line])
        vals = {
            'type': 'sale',
            'date_to_invoice': fields.datetime.today(),
            'invoicefrompicking_line_ids': lines
        }
        print(vals)
        sale_ifpm = ifpm_obj.create(vals)
        
        if len(sale_ifpm.invoicefrompicking_line_ids) > 0:
            who_id = sale_ifpm.id
        else:
            who_id = purchase_ifpm.id

        action = {
            'name': _('%s' % sale_ifpm.name),
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.from.picking.mass',
            'view_mode': 'form',
            'res_id': who_id,
        }

        return action