# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class Cointel_Reparaciones(models.Model):
    _inherit = "repair.order"

    state = fields.Selection(selection_add=[("borrador","Borrador"),("draft",)])
    rma = fields.Many2one('rma', string="RMA")
    estado_rma = fields.Selection(related='rma.state', string="Estado RMA")

    def iniciar_reparacion(self):
        print("******************PRESUPUESTO**********************")
        self.state = 'draft'
        return self