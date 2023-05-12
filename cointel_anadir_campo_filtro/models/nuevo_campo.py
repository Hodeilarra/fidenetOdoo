from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    revisado = fields.Boolean(string='Revisado')