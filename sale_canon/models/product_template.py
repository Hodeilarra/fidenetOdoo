from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    canon_lpi_id = fields.Many2one(
        comodel_name="canon.lpi",
    )
    amount_lpi = fields.Monetary(
        related="canon_lpi_id.amount",
    )
