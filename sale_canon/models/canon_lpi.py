from odoo import fields, models


class CanonLpi(models.Model):
    _name = "canon.lpi"
    _description = "Canon LPI"

    name = fields.Char(
        required=True,
    )
    amount = fields.Monetary(
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="company_id.currency_id",
        readonly=True,
    )
