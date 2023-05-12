from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class albaranes(models.Model):
    _name = 'facturas.albaranes'
    _description = 'Albaranes de Agencia'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'sequence'  # Define el campo 'sequence' como representación del registro

    sequence                      = fields.Char(string='Número', readonly=True, copy=False, default='/')
    customer                      = fields.Many2one('res.partner', string='Cliente', required=True)
    direccion_entrega             = fields.Many2one('res.partner', string='Dirección de entrega', domain="[('parent_id', '=', customer)]")
    fecha_entrega                 = fields.Date('Fecha de entrega solicitada', required=True)
    fecha_confirmacion            = fields.Date('Fecha de entrega confirmada')
    numero_confirmacion_fabrica   = fields.Char(string='Número de confirmación de fábrica')
    numero_pedido_cliente         = fields.Char(string='Número de pedido de cliente')
    supplier_id                   = fields.Many2one('res.partner',string='Proveedor', domain=[('supplier_rank', '>', 0)],help='Selecciona un proveedor')
    albaranes_line_ids            = fields.One2many('facturas.albaranes.line', 'albaranes_id', string='Líneas de Albarán')
    amount_untaxed                = fields.Monetary(string='Base imponible', currency_field='currency_id', compute='_compute_amount')
    amount_tax                    = fields.Float(string='Impuestos', compute='_compute_amount')
    amount_total                  = fields.Float(string='Total', compute='_compute_amount')
    currency_id                   = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    observaciones                 = fields.Text(string='Observaciones')
    status                        = fields.Selection([('draft', 'Borrador'),('confirmed', 'Confirmado'),('posted', 'Publicado'),('cancel', 'Cancelado'),('pending', 'Pendiente de pago'),('archived', 'Archivado')], string='Estado', default='posted')
    related_compra                = fields.Many2one('facturas.sales_compras', string="Presupuesto de compra relacionado", readonly=True)
    x_notes_delivery_agency       = fields.Text(string='Notas de compra')

    
    def create_invoice(self):
        self.ensure_one()
        if self.status != 'confirmed':
            raise ValidationError("Sólo puedes crear una factura para un albarán confirmado.")

        # Crear una nueva factura
        new_invoice = self.env['facturas.invoice'].create({
            'customer': self.customer.id,
            'supplier_id': self.supplier_id.id,
            'factory_order_number': self.numero_confirmacion_fabrica,
            'customer_order_number': self.numero_pedido_cliente,
            'related_document': 'facturas.albaranes,%s' % self.id,
            'x_notes_invoice_agency': self.customer.x_notes_invoice_agency
        })

        # Crear líneas de factura a partir de las líneas de albarán
        for line in self.albaranes_line_ids:
            self.env['facturas.invoice.line'].create({
                'invoice_id': new_invoice.id,
                'product_id': line.product_id.id,
                'quantity': line.cantidad,
                'price_unit': line.precio,
                'discount': line.discount,
                'tax_id': [(6, 0, line.tax_id.ids)],
                'price_subtotal': line.price_subtotal,
                'x_notes_invoice_agency': self.customer.x_notes_invoice_agency
            })

        # Cambiar el estado de albarán a facturado
        self.status = 'confirmed'

        # Redirigir al usuario a la nueva factura
        return {
            'name': 'Factura creada',
            'view_mode': 'form',
            'res_model': 'facturas.invoice',
            'res_id': new_invoice.id,
            'type': 'ir.actions.act_window',
        }

    def action_toggle_archive(self):
        if self.status == 'archived':
            self.status = 'draft'
            
            
        else:
            self.status = 'archived'
            
    
    def action_toggle_confirm(self):
        if self.status == 'confirmed':
            self.status = 'draft'
        else:
            if not self.numero_confirmacion_fabrica:
                raise UserError("No puedes confirmar un albarán sin un número de confirmación de fábrica.")
            self.status = 'confirmed'

            # Actualizar el número de pedido de fábrica en la compra relacionada
            if self.related_compra:
                self.related_compra.numero_confirmacion_fabrica = self.numero_confirmacion_fabrica

                # Si hay una venta relacionada con la compra, actualizar el número de pedido de fábrica en la venta
                if self.related_compra.related_sale:
                    self.related_compra.related_sale.numero_confirmacion_fabrica = self.numero_confirmacion_fabrica
            

    @api.onchange('customer')
    def _onchange_customer(self):
        if self.customer:
            self.direccion_entrega          = self.customer
            self.x_notes_delivery_agency    = self.customer.x_notes_delivery_agency
        else:
            self.direccion_entrega          = False
            self.x_notes_delivery_agency    = False


    @api.depends('albaranes_line_ids.price_subtotal', 'albaranes_line_ids.tax_id', 'albaranes_line_ids.cantidad', 'albaranes_line_ids.precio', 'albaranes_line_ids.discount')
    def _compute_amount(self):
        for albaran in self:
            amount_untaxed = 0.0
            amount_tax = 0.0
            for line in albaran.albaranes_line_ids:
                amount_untaxed += line.price_subtotal
                taxes = line.tax_id.compute_all(line.precio * (1 - (line.discount or 0.0) / 100.0), quantity=line.cantidad)
                amount_tax += sum(tax.get('amount', 0.0) for tax in taxes.get('taxes', []))
            albaran.amount_untaxed = amount_untaxed
            albaran.amount_tax = amount_tax
            albaran.amount_total = amount_untaxed + amount_tax
    
    @api.model
    def create(self, vals):
        if not vals.get('sequence'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('facturas.albaranes') or 0
        self.status = "posted"
        return super(albaranes, self).create(vals)
    
    @api.constrains('sequence')
    def _check_unique_sequence(self):
        for record in self:
            if self.env['facturas.albaranes'].search_count([('sequence', '=', record.sequence)]) > 1:
                raise ValidationError('El número de albarán debe ser único.')



class AlbaranesPickingLine(models.Model):
    _name = 'facturas.albaranes.line'
    _description = 'Línea de albaran'
    
    albaranes_id          = fields.Many2one('facturas.albaranes', string='Albarán')
    customer_id           = fields.Many2one('res.partner', related='albaranes_id.customer', string='Cliente', readonly=True)
    product_id            = fields.Many2one('product.product', string='Producto')
    gramo_metro           = fields.Float(readonly=True, string='g/m²')
    ancho                 = fields.Float(string='Ancho (mm)', default=1.0)
    cantidad              = fields.Float(string='Cantidad (kgs)', required=True, default=1.0)
    precio                = fields.Float(string='Precio (€/kg)')
    fecha_entrega         = fields.Char('Fecha Entrega')
    mand                  = fields.Float(related='customer_id.mand', string='Mand. (mm)', readonly=False)
    diametro              = fields.Float(related='customer_id.diametro', string='Diam.Ex. (cm)', readonly=False)
    discount              = fields.Float(string='Descuento (%)')
    tax_id                = fields.Many2many('account.tax', string='Impuestos')
    price_subtotal        = fields.Float(string='Subtotal (€)', compute='_compute_subtotal', store=True)



    @api.depends('cantidad', 'precio', 'discount')
    def _compute_subtotal(self):
        for line in self:
            price = line.precio * (1 - (line.discount or 0.0) / 100.0)
            line.price_subtotal = price * line.cantidad

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.precio      = self.product_id.list_price
            self.gramo_metro = self.product_id.weight
        else:
            self.precio = 0.0
            self.gramo_metro = 0.0