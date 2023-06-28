from odoo import fields, models, api

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    project_id = fields.One2many('project.project', 'analytic_account_id', string="Project")
    presupuestos_asociados = fields.Many2one(
        'sale.order', 
        string='Presupuesto Asociado',
        compute='_compute_presupuestos_asociados'
    )

    @api.depends('project_id')
    def _compute_presupuestos_asociados(self):
        for rec in self:
            if rec.project_id and rec.project_id.presupuesto_asociado:
                # Buscar todas las órdenes de venta (presupuestos) que tengan el mismo prefijo en el nombre.
                presupuesto_prefix = rec.project_id.presupuesto_asociado.name
                rec.presupuestos_asociados = self.env['sale.order'].search([('name', 'like', presupuesto_prefix+'%')]).ids
            else:
                rec.presupuestos_asociados = False