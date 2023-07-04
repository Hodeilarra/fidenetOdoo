from odoo import api, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        # Primero llamamos al método original
        result = super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        
        

        # Aquí va el código personalizado que quieres añadir
        canon = self.env.ref("sale_canon.product_canon_lpi")
        for sale in self:
            if not sale.partner_id._get_client_is_excluded():
                sale.order_line.filtered(
                    lambda x: x.product_id == canon).unlink()
                sale.order_line.filtered(
                    lambda x: x.product_id != canon)._update_canon_lpi()
            else:
                sale.order_line.filtered(
                    lambda x: x.product_id == canon).unlink()

        return result