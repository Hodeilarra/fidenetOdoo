from odoo import fields, models, api
import logging


class SaleOrderProforma(models.Model):
    _inherit = 'sale.order'

    proforma = fields.Boolean(string='Proforma')
    


    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrderProforma, self).default_get(fields_list)
        print(str(self.env.context.get('from_proforma_view')))
        if self.env.context.get('from_proforma_view'):
            res['type_id'] = 2
        return res
