# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class Cointel_Cancel_Account(models.Model):
    _inherit = "account.move"

    payment_state = fields.Selection(selection_add=[
        ('cancel', 'Cancelado')
    ])

    def write(self, vals):
        self = super(Cointel_Cancel_Account, self).create(vals)
        
        return self