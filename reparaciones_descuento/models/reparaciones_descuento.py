# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ReparacionesDescuento(models.Model):
	_inherit = 'repair.line'

	descuento = fields.Float(string='Descuento')

	def write(self, vals):
		res = super().write(vals)
		print('*****************************GuardadoDescuento*****************************')
		reparacion = self.env['repair.order'].search([('id', '=', self.repair_id.id)])
		for linea in reparacion.operations:
			#linea.price_subtotal = linea.price_unit*(100-linea.descuento)
			print("*****************************"+str(linea.price_subtotal)+"*****************************")
			print("*****************************"+str(linea.descuento)+"*****************************")
			print("*****************************"+str(linea.price_unit*(1-(linea.descuento/100)))+"*****************************")
			linea.price_subtotal = linea.price_unit*(1-(linea.descuento/100))
			print("**********************************************************")