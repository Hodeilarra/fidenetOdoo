from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tecnico_id = fields.Many2one('res.users', string='Técnico')
