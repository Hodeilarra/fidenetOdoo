# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools

class ReadCodePos(models.Model):
	_inherit = 'pos.session'

	def my_button(self):
		print("###########################*************AAAAAAAAAA***********##############################")