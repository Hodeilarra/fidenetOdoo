from odoo import fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    presupuesto_asociado = fields.Many2one('sale.order', string='Presupuesto', readonly=True)

    