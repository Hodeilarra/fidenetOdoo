from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _create_canon_line(self, values):
        Line = self.env["sale.order.line"]
        canon = self.env.ref("sale_canon.product_canon_lpi")
        description = "{}\n".format(canon.name) + "\nDesglose de los canones:"
        amount = 0
        for product in values:
            description += _("\n{} de {} x {} = {}".format(
                values[product],
                product.default_code or product.display_name,
                product.canon_lpi_id.amount,
                values[product] * product.canon_lpi_id.amount,
            ))
            amount += values[product] * product.canon_lpi_id.amount
        Line.create({
            "sequence": (self[-1:].sequence + 1) or 999,
            "product_id": canon.id,
            "product_uom_qty": 1,
            "order_id": self[:1].order_id.id,
            "name": description,
            "price_unit": amount,
        })

    def _update_canon_lpi(self):
        lines = self.filtered(lambda x: x.product_id.canon_lpi_id)
        if not lines:
            return
        values = {}
        for line in lines:
            if line.product_id not in values:
                values[line.product_id] = line.product_uom_qty
            else:
                values[line.product_id] += line.product_uom_qty
        lines._create_canon_line(values)
