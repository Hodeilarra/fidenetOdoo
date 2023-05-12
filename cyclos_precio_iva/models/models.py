# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RepairOrder(models.Model):
	_inherit = 'repair.line'

	precio_iva = fields.Monetary(string="Precio con IVA")

	@api.onchange("precio_iva")
	def precio_iva_modify(self):
		print("kaixo")
		self.price_unit = (self.precio_iva/1.21)
		print(self.price_unit)
		print(self.precio_iva)


	@api.onchange("price_unit")
	def precio_unitario(self):
		print("kaixo2")
		self.precio_iva = (self.price_unit*1.21)
		print(self.price_unit)
		print(self.precio_iva)