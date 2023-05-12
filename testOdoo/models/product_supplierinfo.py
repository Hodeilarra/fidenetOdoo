# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    def write(self, vals):
        res = super().write(vals)
        if 'name' in vals:
            self._check_cost_price_on_list_price()
        return res

    def _check_cost_price_on_list_price(self):
        for p in self:
            if p.name.descuento_boolean:
                p.price = p.name.compute_new_price(p.product_tmpl_id.list_price)
