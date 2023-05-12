# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class TaskInvoiceLine(models.Model):
    _name = "custom.task.invoice.line"
    _description = "Task Invoice Line"
    
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
    )
    name = fields.Text(
        string="Descripción"
    )
    quantity = fields.Float(
        string='Cantidad',
        digits='Product Unit of Measure',
        default=1
    )
    product_uom_qty = fields.Float(
        string='Product UOM Quantity', 
        digits='Product Unit of Measure',
        default=1.0,
    )
    product_uom = fields.Many2one(
        'uom.uom',
        string='Unidad de medida',
    )
    custom_task_id = fields.Many2one(
        'project.task',
        string='Task Invoice',
        copy=False
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account'
    )
    is_invoice = fields.Boolean(
        string='Is Invoice Created',
        default=False,
        copy=False,
        readonly=True
    )
    custom_invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        copy=False
    )
    custom_invoice_line_id = fields.Many2one(
        'account.move.line',
        string='Invoice Line',
        readonly=True,
        copy=False
    )
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    _order = "sequence,id"
    sequence = fields.Integer(default=10,help="Gives the sequence order when displaying a list of records.")

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}
        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
            vals['product_uom'] = self.product_id.uom_id.id
        #vals['name'] = self.product_id.name
        self.update(vals)
        return {'domain': domain}
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
