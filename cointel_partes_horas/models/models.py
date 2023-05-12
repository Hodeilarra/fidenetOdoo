# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    ticket_id = fields.Many2one(
        comodel_name="helpdesk.ticket",
        string="Ticket",
        domain=[("project_id", "!=", False)],
        groups="helpdesk_mgmt.group_helpdesk_user",
    )
    
    description = fields.Html(
        comodel_name="helpdesk.ticket",
        related="ticket_id.description",
        string="Descripción del ticket",
    )

    @api.onchange("ticket_id")
    def onchange_ticket_id(self):
        for record in self:
            if not record.ticket_id:
                continue
            record.project_id = record.ticket_id.project_id
            record.task_id = record.ticket_id.task_id
            record.description = record.ticket_id.description
	
	


	