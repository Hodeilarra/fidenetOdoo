# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleValorModify(models.Model):
	_inherit = 'sale.order'

	valor = fields.Selection([('si', 'Si'), ('no', 'No')], string='DT', tracking=True, default='si', required='True')

	valorBoton = fields.Boolean(string="ValorBoton", compute="_set_valorBoton", store=False)

	proyectoPresupuesto = fields.Many2one('project.project', string="Proyecto")

	def _get_cuentasBancarias(self):
		company = self.env['res.partner'].search([('name', '=', 'COINTEL S.L.')]) #Nombre del contacto
		lst = []
		for bank_id in company.bank_ids:
			lst.append((bank_id.display_name, bank_id.display_name))
		return lst

	cuentasAsociadas = fields.Selection(_get_cuentasBancarias, string='Cuentas Bancarias')

	@api.depends('valor','state')
	def _set_valorBoton(self):
		valorB = dict(self._fields['valor'].selection).get(self.valor)
		valorEstado = dict(self._fields['state'].selection).get(self.state)
		if (valorB == "Si" and valorEstado == "Sales Order" and not self.proyectoPresupuesto):
			self.valorBoton = False
		else:
			self.valorBoton = True
	
	def pick_one(self):
		primerEstado = False
		projectStatuses = self.env['project.status'].search([])
		for status in projectStatuses:
			if(primerEstado == False):
				estadoProyecto = status
				primerEstado = True
		proyecto_id = self.env['project.project'].create({
			'name': str(self.partner_id.name),
			'project_status': estadoProyecto.id,
			'partner_id': self.partner_id.id
		})
		self.proyectoPresupuesto = proyecto_id

class SaleTableModify(models.Model):
	_inherit = "sale.order.line"

	valor = fields.Selection([('si', 'Si'), ('no', 'No')], string='DT', readonly='True')

class StockTableModify(models.Model):
	_inherit = 'stock.picking'

	sale_id = fields.Many2one('sale.order')
	valor = fields.Selection([('si', 'Si'), ('no', 'No')], string='DT', related='sale_id.valor', readonly=False, store_true=True)

	hide = fields.Boolean(string="Hide", compute="_set_hide", store=False)

	@api.depends('sale_id')
	def _set_hide(self):
		if self.sale_id.id:
			self.hide = False
		else:
			self.hide = True

class ProjectModify(models.Model):
	_inherit = 'project.project'

	def action_view_sales(self):
		action = self.env['ir.actions.actions']._for_xml_id("sale.action_orders")
		action['domain'] = [('invoice_status', '=', 'sale')and('proyectoPresupuesto', '=', self.id)]
		return action

	def action_create_project_sales(self):
		user = self.env.user
		vals = {
			'proyectoPresupuesto' : self.id,
			'partner_id' : self.partner_id.id
		}
		nuevoPresupuesto = self.env['sale.order'].create(vals)
		context = dict(self.env.context)
		context['form_view_initial_mode'] = 'edit'
		return	{
					'type' : 'ir.actions.act_window',
					'view_type' : 'form',
					'view_mode' : 'form',
					'res_model' : 'sale.order',
					'res_id' : nuevoPresupuesto.id,
					'context' : context
				}
