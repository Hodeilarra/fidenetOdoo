# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools

class SaleOrderForm(models.Model):
	_inherit = 'sale.order'

	repair_id = fields.Many2one('repair.order', string="Reparación")

	ocultar = fields.Boolean(string="Ocultar", compute="_hide_repair")

	@api.depends('repair_id')
	def _hide_repair(self):
		if self.repair_id.id:
			self.ocultar = False
		else:
			self.ocultar = True