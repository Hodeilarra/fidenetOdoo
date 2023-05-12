# -*- coding: utf-8 -*

from odoo import models, fields, api , _
from odoo.exceptions import UserError
from datetime import datetime

class Project(models.Model):
    _inherit = 'project.project'

    presupuesto = fields.Many2one('sale.order', string="Presupuesto")
    
    def action_edit_project(self, context=None):
        project = self.env['project.project'].search([('name', '=', self.name)])
        if not context:
            context = {}

        name = project.name
        res_model = 'project.project'

        return {
            'name': (name),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('project.edit_project').id,
            'res_model': res_model, 
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': project.id,
        }
    

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    custom_invoice_line_ids = fields.One2many(
        'custom.task.invoice.line',
        'custom_task_id',
        string='Mediciones',
        copy=True
    )
    custom_inv_journal_id = fields.Many2one(
        'account.journal',
        string='Diario de facturas',
        default=1,
        copy=True
    )
    custom_inv_user_id = fields.Many2one(
        'res.users',
        default=2,
        string="Usuario de factura"
    )
    presupuesto = fields.Many2one('sale.order', string="Presupuesto")
    

    def action_create_sale(self):
        if(not self.project_id.presupuesto.id):
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            sale_id = self.env['sale.order'].create(    
				{'partner_id': self.partner_id.id,
				'task_id': self.id,
                'project_id': self.project_id.id,     
				'date_order': dt_string,
                'nombreObra': self.project_id.name,      
				'picking_policy': 'direct'
				})
            self.project_id.presupuesto = sale_id
        if(not self.presupuesto.id):
            self.env['sale.order.line'].create({
                            'display_type': 'line_section',
                            'name': self.name,
                            'order_id': self.project_id.presupuesto.id
                        })
            for product in self.custom_invoice_line_ids :
                productV = product.product_id
                if not productV:
                    valorDisplay = dict(product._fields['display_type'].selection).get(product.display_type)
                    if(str(valorDisplay)=='Section'):
                        self.env['sale.order.line'].create({
                            'display_type': 'line_section',
                            'name': product.name,
                            'order_id': self.project_id.presupuesto.id
                        })
                    else:
                        self.env['sale.order.line'].create({
                            'display_type': 'line_note',
                            'name': product.name,
                            'order_id': self.project_id.presupuesto.id
                        })
                else:
                    self.env['sale.order.line'].create({  
                                'product_id': productV.id,
                                'name': productV.display_name or " ",
                                'product_uom_qty': product.quantity,
                                'product_uom': product.product_uom.id,
                                'order_id': self.project_id.presupuesto.id
                            })
            self.presupuesto = self.project_id.presupuesto
        else:
            #Actualizar lista
            sale = self.env['sale.order'].search([('id', '=', self.presupuesto.id)])
            saleorderline = self.env['sale.order.line'].search([('order_id', '=', sale.id)])
            for product in saleorderline:
                product.unlink()

            project = self.env['project.project'].search([('id', '=', self.project_id.id)])
            for task in reversed(project.task_ids):
                self.env['sale.order.line'].create({
                            'display_type': 'line_section',
                            'name': task.name,
                            'order_id': task.project_id.presupuesto.id
                        })
                for product in task.custom_invoice_line_ids :
                    productV = product.product_id
                    if not productV:
                        valorDisplay = dict(product._fields['display_type'].selection).get(product.display_type)
                        if(str(valorDisplay)=='Section'):
                            self.env['sale.order.line'].create({
                                'display_type': 'line_section',
                                'name': product.name,
                                'order_id': task.project_id.presupuesto.id
                            })
                        else:
                            self.env['sale.order.line'].create({
                                'display_type': 'line_note',
                                'name': product.name,
                                'order_id': task.project_id.presupuesto.id
                            })
                    else:
                        self.env['sale.order.line'].create({  
                                'product_id': productV.id,
                                'name': product.name or " ",
                                'product_uom_qty': product.quantity,          
                                'order_id': task.project_id.presupuesto.id
                            })

        return self
        
    
    def show_invoice_custom(self):
        self.ensure_one()
        res = self.env.ref('account.action_move_out_invoice_type')
        res = res.read()[0]
        res['domain'] = [('custom_task_probc_id','=', self.id)]
        return res