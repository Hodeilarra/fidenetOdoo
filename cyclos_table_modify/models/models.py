# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CyclosTableModify(models.Model):
	_inherit = 'repair.line'

	precio_iva = fields.Monetary(string='Precio Con IVA')
	repeticion = fields.Integer(default=0)

	@api.onchange('precio_iva')
	def precio_iva_modify(self):
		self.repeticion = 1
		self.price_unit = (self.precio_iva / 1.21)
	
	@api.onchange('price_unit')
	def price_unit_modify(self):
		if self.repeticion == 0:
			self.precio_iva = (self.price_unit * 1.21)