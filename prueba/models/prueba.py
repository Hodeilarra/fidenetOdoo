# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models

class prueba(models.Model):
    _inherit = "res.partner"

    fechaNacimiento = fields.data(string="Fecha de nacimiento:", required=True)
    edad = fields.date.Today - fechaNacimiento
    edadUsuario = fields.Integer(string="Edad:", required=True)


