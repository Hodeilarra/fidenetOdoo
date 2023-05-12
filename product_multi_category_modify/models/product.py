# Copyright 2009 Akretion,Guewen Baconnier,Camptocamp,Avanzosc,Sharoon Thomas,Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_id = fields.Many2one(
        'product.category',
        string="Categorias",
    )
