# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	dt = fields.Selection([('si', 'Si'), ('no', 'No')], string='DT', tracking=True, default='si', required='True')

	


	