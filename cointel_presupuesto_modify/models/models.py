# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrderRepair(models.Model):
	_inherit = 'sale.order'

	presupuesto = fields.Many2one('sale.order', string="Presupuesto")

def write(self, vals):
	res = super().write(vals)
	
	


	