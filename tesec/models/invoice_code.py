# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools

class InvoiceCode(models.Model):
	_inherit = 'account.move'

	presupuesto = fields.Many2one('sale.order')

	nombreObra = fields.Char(related='presupuesto.nombreObra')

	@api.model
	def create(self, vals):
		self = super(InvoiceCode, self).create(vals)
		sale = self.env['sale.order'].search([('name', '=', self.invoice_origin)])
		self.presupuesto = sale.id
		return self