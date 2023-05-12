from odoo import fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', help='Related Opportunity for this project', domain=[('type', '=', 'opportunity')])
