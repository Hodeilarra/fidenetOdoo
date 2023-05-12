# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools
from datetime import datetime
from barcode import EAN13
import random

class UpdateRepair(models.Model):
	_inherit = 'repair.order'

	presupuesto = fields.Many2one('sale.order', string="Presupuesto")

	def write(self, vals):
		res = super().write(vals)
		#Actualizar descripciion del sale.order.line
		sale = self.env['sale.order'].search([('id', '=', self.presupuesto.id)])
		saleorderline = self.env['sale.order.line'].search([('order_id', '=', sale.id)])
		i=0
		for product in saleorderline:
			if(product.name != self.operations[i].name):
				product.name = self.operations[i].name
			i += 1
		#Actualizar el estado de sale.order
		sale = self.env['sale.order'].search([('id', '=', self.presupuesto.id)])
		if(str(self.state) == "confirmed"):
				sale.state = 'sale'
		if(str(self.state) == "cancel"):
				sale.state = self.state
		return res

	@api.model
	def create(self, vals):
		self = super(UpdateRepair, self).create(vals)
		#Crear un presupuesto asociado a la reparacion
		now = datetime.now()
		dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
		sale_id = self.env['sale.order'].create(    
			{'partner_id': self.partner_id.id,
			'repair_id': self.id,     
			'date_order': dt_string,     
			'picking_policy': 'direct'
			})

		for product in self.operations :
			self.env['sale.order.line'].create({  
					'product_id': product.product_id.id,
					'name': product.name,
					'product_uom_qty': product.product_uom_qty,
					'price_unit': product.price_unit,             
					'order_id': sale_id.id
				})
		self.presupuesto = sale_id
		return self
