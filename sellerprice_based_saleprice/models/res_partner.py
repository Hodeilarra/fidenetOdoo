# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class ResPartner(models.Model):
    _inherit = "res.partner"

    cost_price_on_list_price = fields.Boolean(string="Cost price on sale price",
                                              help="Is cost price based on sale price? a discount can be applied")
    cost_price_on_list_price_discount = fields.Float(string="% Discount on Sale price",
                                                     help="If purchase price is based on sale price, the configured"
                                                          " discount in this field will be applied to sale price and "
                                                          "stored in cost price and seller price")

    def write(self, vals):
        res = super().write(vals)
        if 'cost_price_on_list_price' in vals or 'cost_price_on_list_price_discount' in vals:
            self._check_cost_price_on_list_price()
        return res

    def _check_cost_price_on_list_price(self):
        for p in self:
            if p.cost_price_on_list_price:
                """Buscamos todos los productos del proveedor"""
                sellerids = p.find_seller_products()
                """Le aplicamos el descuento y lo guardamos en seller_ids y el standad_price"""
                for s in sellerids:
                    # Ver si se puede configurar algo en variables del sistema para el cálculo del descuento.
                    price = self.compute_new_price(s.product_tmpl_id.list_price)
                    s.product_tmpl_id.standard_price = price
                    s.price = price
                """FIN"""

    def find_seller_products(self):
        return self.env['product.supplierinfo'].search([('name', 'in', self.ids)])

    def compute_new_price(self, list_price):
        return list_price * (1-self.cost_price_on_list_price_discount/100)

