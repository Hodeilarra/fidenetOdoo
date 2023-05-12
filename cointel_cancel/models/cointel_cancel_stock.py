# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class Cointel_Cancel_Stock(models.Model):
    _inherit = "stock.picking"



    def write(self, vals):
        self = super(Cointel_Cancel_Stock, self).create(vals)
        
        return self