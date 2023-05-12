# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools
from barcode import EAN13
import random

class BarCode(models.Model):
    _inherit = "repair.order"

    def get_code(self):
        numero = random.randint(100000000000, 999999999999)
        code = str(numero)
        return code

    codigo_barras = fields.Char(string="Código de barras", default=get_code)

    def write(self, vals):
        res = super().write(vals)
        return res