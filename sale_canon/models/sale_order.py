from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, values):
        canon = self.env.ref("sale_canon.product_canon_lpi")
        sales = super().write(values)
        for sale in self:
            if not sale.partner_id._get_client_is_excluded():
                sale.order_line.filtered(
                    lambda x: x.product_id == canon).unlink()
                sale.order_line.filtered(
                    lambda x: x.product_id != canon)._update_canon_lpi()
            else:
                sale.order_line.filtered(
                    lambda x: x.product_id == canon).unlink()
        return sales

    @api.model
    def create(self, values):
        canon = self.env.ref("sale_canon.product_canon_lpi")
        sale = super().create(values)
        if not sale.partner_id._get_client_is_excluded():
            sale.order_line.filtered(lambda x: x.product_id == canon).unlink()
            sale.order_line.filtered(
                lambda x: x.product_id != canon)._update_canon_lpi()
        return sale
