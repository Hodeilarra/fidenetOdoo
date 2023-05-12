# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ReparacionesDescuento(models.Model):
	_inherit = 'repair.line'

	descuento = fields.Float(string='Descuento')

	@api.depends('price_unit','descuento')
	def _compute_price_subtotal(self):
		for linea in self:
			linea.price_subtotal = linea.price_unit * (1 - (linea.descuento or 0.0) / 100.0)