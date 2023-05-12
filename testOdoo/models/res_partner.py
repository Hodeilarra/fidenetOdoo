# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class ResPartner(models.Model):
    _inherit = "res.partner"

    descuento_boolean = fields.Boolean(string="Aplicar descuento", help="Aplicar descuento")

    coste_descuento = fields.Float(string="% Descuento en el precio de venta", help="% Descuento en el precio de venta")


    def write(self, vals):
        res = super().write(vals)
        if 'descuento_boolean' in vals or 'coste_descuento' in vals:
            self._check_cost_price_on_list_price()
        return res

    def _check_cost_price_on_list_price(self):
        for p in self:
            if p.descuento_boolean:
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
        return list_price * (1-self.coste_descuento/100)

