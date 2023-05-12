# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools

class SaleCode(models.Model):
	_inherit = 'sale.order'

	task_id = fields.Many2one('project.task', string="Tarea")
	project_id = fields.Many2one('project.project')
	nombreObra = fields.Char(related='project_id.name', string="Nombre de obra")
