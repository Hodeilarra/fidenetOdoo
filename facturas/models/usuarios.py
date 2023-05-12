from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    mand                                      = fields.Float(string='Mand (mm)')
    diametro                                  = fields.Float(string='Diam.Ex. (cm)')
    x_notes_sale_agency                       = fields.Text(string='Notas de venta de agencia')
    x_notes_purchase_agency                   = fields.Text(string='Notas de compra de agencia')
    x_notes_invoice_agency                    = fields.Text(string='Notas de factura de agencia')
    x_notes_delivery_agency                   = fields.Text(string='Notas de albarán de agencia')
    custom_sales_ventas_ids                   = fields.One2many('facturas.sales_ventas', 'customer', string='Presupuestos de venta')
    custom_sales_ventas_count                 = fields.Integer(string='Presupuestos totales venta', compute='_compute_custom_sales_ventas_count')
        
    custom_sales_compras_ids                  = fields.One2many('facturas.sales_compras', 'customer', string='Presupuestos de compra')
    custom_sales_compras_count                = fields.Integer(string='Presupuestos totales compra', compute='_compute_custom_sales_compras_count')


    custom_facturas_cliente_ids               = fields.One2many('facturas.invoice', 'customer', string='Facturas cliente')
    custom_facturas_cliente_total             = fields.Float(string='Facturas totales cliente', compute='_compute_custom_facturas_cliente_count')

    custom_facturas_proveedor_ids             = fields.One2many('facturas.invoice', 'supplier_id', string='Facturas proveedor')
    custom_facturas_proveedor_total           = fields.Float(string='Facturas totales proveedor', compute='_compute_custom_facturas_proveedor_count')
    
    

    def _compute_custom_sales_ventas_count(self):
        for partner in self:
            partner.custom_sales_ventas_count = self.env['facturas.sales_ventas'].search_count([('customer', '=', partner.id)])


    def _compute_custom_sales_compras_count(self):
        for partner in self:
            partner.custom_sales_compras_count = self.env['facturas.sales_compras'].search_count([('customer', '=', partner.id)])

    
    def _compute_custom_facturas_cliente_count(self):
        for partner in self:
            
            invoices = self.env['facturas.invoice'].search([('customer', '=', partner.id)])
            partner.custom_facturas_cliente_total   = sum(invoice.amount_total for invoice in invoices)


    def _compute_custom_facturas_proveedor_count(self):
        for partner in self:
            
            invoices = self.env['facturas.invoice'].search([('supplier_id', '=', partner.id)])
            partner.custom_facturas_proveedor_total   = sum(invoice.amount_total for invoice in invoices)


    
            

           

    def action_view_custom_sales_ventas(self):
        self.ensure_one()
        #purchases = self.env['facturas.sales_compras'].search([('related_sale', '=', self.id)])
        purchases = self.env['facturas.sales_ventas'].search([('customer', '=', self.id)])
       
        return {
            'name': 'Presupuestos de venta Agencia de '+self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'facturas.sales_ventas',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', purchases.ids)],
            
            'target': 'current',
        }


    def action_view_custom_sales_compras(self):
        self.ensure_one()
        #purchases = self.env['facturas.sales_compras'].search([('related_sale', '=', self.id)])
        purchases = self.env['facturas.sales_compras'].search([('customer', '=', self.id)])
       
        return {
            'name': 'Presupuestos de compra Agencia de '+self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'facturas.sales_compras',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', purchases.ids)],
            
            'target': 'current',
        }

    def action_view_custom_facturas_cliente(self):
        self.ensure_one()
        
        purchases = self.env['facturas.invoice'].search([('customer', '=', self.id)])
       
        return {
            'name': 'Facturas de cliente Agencia de '+self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'facturas.invoice',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', purchases.ids)],
            
            'target': 'current',
        }


    def action_view_custom_facturas_proveedor(self):
        self.ensure_one()
        
        purchases = self.env['facturas.invoice'].search([('supplier_id', '=', self.id)])
       
        return {
            'name': 'Facturas de proveedor Agencia de '+self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'facturas.invoice',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', purchases.ids)],
            
            'target': 'current',
        }