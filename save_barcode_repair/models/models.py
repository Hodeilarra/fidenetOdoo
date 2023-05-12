# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools

class UpdateRepair(models.Model):
	_inherit = 'repair.order'

	print('*****************************************AAA*************************************************')

	def write(self, vals):
		print('*************************************************Actualizando datos*************************************************')
		override_write  = super(UpdateRepair, self).write(vals)
		print('*************************************************Datos actualizados*************************************************')
		return override_write

