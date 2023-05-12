# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools

class UrlCode(models.Model):
    _inherit = "repair.order"
    
    codigo_url = fields.Many2one('sale.order', string='codigo', required=True)