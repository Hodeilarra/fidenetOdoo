from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    id_transaccion = fields.Char(string='ID Transacción', readonly=True)
