# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        res = super().write(vals)
        if 'list_price' in vals or 'seller_ids' in vals:
            self._check_cost_price_on_list_price()
        return res

    def _check_cost_price_on_list_price(self):
        for p in self:
            for seller in p.seller_ids:
                if seller.name.descuento_boolean:
                    price = seller.name.compute_new_price(p.list_price)
                    seller.price = price
                    p.standard_price = price
