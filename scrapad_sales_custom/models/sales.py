from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    id_transaccion = fields.Char(string='ID Transacción', readonly=True)
    margin = fields.Float(string='Margin', currency_field='currency_id')


    @api.model
    def create(self, vals):
        record = super(SaleOrder, self).create(vals)
        record.action_confirm()
        return record