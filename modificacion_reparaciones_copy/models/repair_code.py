# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools
from datetime import datetime
#from barcode import EAN13
import random

class UpdateRepair(models.Model):
	_inherit = 'repair.order'

	codigo_barras = fields.Char(string="Código de barras")
	presupuesto = fields.Many2one('sale.order', string="Presupuesto")

	def copy(self, default=None):
		default = dict(default or {})
		numero = random.randint(100000000000, 999999999999)
		code = str(numero)
		numeroCodigo = code
		#Comprobar que no se repitan los codigos de barras
		repairs = self.env['repair.order'].search([])
		i=0
		while i < len(repairs):
			if (numeroCodigo != repairs[i].codigo_barras):
				i += 1
			else:
				numero = random.randint(100000000000, 999999999999)
				code = str(numero)
				numeroCodigo = code
				i = 0
		default.update({'codigo_barras': numeroCodigo}) 
		self = super(UpdateRepair, self).copy(default)
		
		#Crear un presupuesto asociado a la reparacion
		now = datetime.now()
		dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
		sale_id = self.env['sale.order'].create(    
			{'partner_id': self.partner_id.id,
			'codigo_barras': self.codigo_barras, 
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

	def write(self, vals):
		res = super().write(vals)
		print('*****************************WRITE*****************************')
		#Actualizar productos y descripciion del sale.order
		if(self.presupuesto.id and str(self.state) == "draft"):
			sale = self.env['sale.order'].search([('id', '=', self.presupuesto.id)])
			saleorderline = self.env['sale.order.line'].search([('order_id', '=', sale.id)])
			for product in saleorderline:
				product.unlink()

			for product in self.operations:
				self.env['sale.order.line'].create({  
				'product_id': product.product_id.id,
				'name': product.name,
				'product_uom_qty': product.product_uom_qty,
				'price_unit': product.price_unit,             
				'order_id': sale.id
				})

		#Actualizar el estado de sale.order
		sale = self.env['sale.order'].search([('id', '=', self.presupuesto.id)])
		if(str(self.state) == "confirmed"):
				sale.state = 'sale'
		if(str(self.state) == "cancel"):
				sale.state = self.state
		if(str(self.state) == "done"):
				sale.state = self.state
		return res

	@api.model
	def create(self, vals):
		self = super(UpdateRepair, self).create(vals)
		print('*****************************CREATE*****************************')
		sale = self.env['sale.order'].search([('id', '=', self.presupuesto.id)])
		if(not self.presupuesto.id):
			#Comprobar que no se repitan los codigos de barras
			repairs = self.env['repair.order'].search([])
			i=2
			while i < len(repairs):
				if (self.codigo_barras != repairs[i].codigo_barras):
					i += 1
				else:
					numero = random.randint(100000000000, 999999999999)
					code = str(numero)
					self.codigo_barras = code
					i = 2
			#Crear un presupuesto asociado a la reparacion
			now = datetime.now()
			dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
			sale_id = self.env['sale.order'].create(    
				{'partner_id': self.partner_id.id,
				'codigo_barras': self.codigo_barras, 
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
