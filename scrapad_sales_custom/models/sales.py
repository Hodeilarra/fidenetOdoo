from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    id_transaccion = fields.Char(string='ID Transacción', readonly=True)


    @api.model
    def create(self, vals):
        record = super(SaleOrder, self).create(vals)
        record.action_confirm()
        return record