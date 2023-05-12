# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleValorModify(models.Model):
	_inherit = 'sale.order'

	valor = fields.Selection([('si', 'Si'), ('no', 'No')], string='DT', tracking=True, default='si')

class SaleTableModify(models.Model):
	_inherit = "sale.order.line"

	valor = fields.Selection([('si', 'Si'), ('no', 'No')], string='DT', readonly='True')

class StockTableModify(models.Model):
	_inherit = 'stock.picking'

	sale_id = fields.Many2one('sale.order')
	valor = fields.Selection([('si', 'Si'), ('no', 'No')], string='DT', related='sale_id.valor', readonly=False, store_true=True)

	hide = fields.Boolean(string="Hide", compute="_set_hide", store=False)

	@api.depends('sale_id')
	def _set_hide(self):
		if self.sale_id.id:
			self.hide = False
		else:
			self.hide = True