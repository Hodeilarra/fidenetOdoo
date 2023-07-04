# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models, tools
from datetime import datetime

class SaleCode(models.Model):
	_inherit = 'sale.order'

	task_id = fields.Many2one('project.task', string="Tarea")
	task_name = fields.Char(string="Nombre de Tarea", compute="_compute_task_name")

	project_id = fields.Many2one('project.project', string="Obra asociada")
	nombreObra = fields.Char(related='project_id.name', string="Nombre de obra")
	fecha_creacion_tarea = fields.Date(related='task_id.fecha_creacion', string='Fecha de creación de la tarea', readonly=True, store=True)
	notas = fields.Char(string="Notas")


	#def _prepare_invoice(self):
	#	invoice_vals = super(SaleCode, self)._prepare_invoice()
	#	invoice_vals.update({
	#		'nombreObra': "1",
	#		'proyecto': "2",
	#		'ref': "3"
	#	})
	#	return invoice_vals

	@api.depends('task_id')
	def _compute_task_name(self):
	    for record in self:
	        record.task_name = record.task_id.name

	@api.depends('task_name')
	def _compute_task_date(self):
	    for record in self:
	        if record.task_name:
	            try:
	                # Primero intentamos con el formato dd-mm-yyyy
	                date_object = datetime.strptime(record.task_name, '%d-%m-%Y').date()
	            except ValueError:
	                try:
	                    # Si falla, intentamos con el formato dd-mm-yy
	                    date_object = datetime.strptime(record.task_name, '%d-%m-%y').date()
	                except ValueError:
	                    # Si ambos formatos fallan, dejamos el campo como False (vacio)
	                    date_object = False
	            record.task_date = date_object

	def _prepare_invoice(self):
		invoice_vals = super(SaleCode, self)._prepare_invoice()

		selected_orders = self.env.context.get('active_ids', [])
		if selected_orders:
			orders = self.browse(selected_orders)

			nombre_obra = ', '.join(order.nombreObra for order in orders if order.nombreObra)
			proyectos = orders.mapped('project_id')  # Obtiene todos los proyectos distintos asociados a los presupuestos
			ref = ', '.join(order.client_order_ref for order in orders if order.client_order_ref)

			

			invoice_vals.update({
				'nombreObra': nombre_obra[0] if nombre_obra else False,
				'proyecto': proyectos[0].id if proyectos else False,  # Utiliza el primer proyecto encontrado, si hay alguno
				'ref': ref
			})

		return invoice_vals

	
