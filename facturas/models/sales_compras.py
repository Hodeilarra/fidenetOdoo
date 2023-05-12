from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class sales_compras(models.Model):
    _name = 'facturas.sales_compras'
    _description = 'Allows you to define the characteristics of an invoice'
    _rec_name = 'sequence'  # Define el campo 'sequence' como representación del registro
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    sequence                      = fields.Char(string='Número', readonly=True, copy=False, default='/')
    customer                      = fields.Many2one('res.partner', string='Cliente', required=True)
    direccion_entrega             = fields.Many2one('res.partner', string='Dirección de entrega', domain="[('parent_id', '=', customer)]")
    fecha_entrega                 = fields.Date('Fecha de entrega solicitada', required=True)
    fecha_confirmacion            = fields.Date('Fecha de entrega confirmada')
    numero_confirmacion_fabrica   = fields.Char(string='Número de confirmación de fábrica')
    numero_pedido_cliente         = fields.Char(string='Número de pedido de cliente')
    supplier_id                   = fields.Many2one('res.partner',string='Proveedor', domain=[('supplier_rank', '>', 0)],help='Selecciona un proveedor')
    sales_compras_line_ids        = fields.One2many('facturas.sales_compras.line', 'sales_compras_id', string='Líneas de Presupuesto')
    amount_untaxed                = fields.Monetary(string='Base imponible', currency_field='currency_id', compute='_compute_amount')
    amount_tax                    = fields.Float(string='Impuestos', compute='_compute_amount')
    amount_total                  = fields.Float(string='Total', compute='_compute_amount')
    currency_id                   = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    observaciones                 = fields.Text(string='Observaciones')
    status                        = fields.Selection([('draft', 'Borrador'),('confirmed', 'Confirmado'),('posted', 'Publicado'),('cancel', 'Cancelado'),('pending', 'Pendiente de pago'),('archived', 'Archivado')], string='Estado', default='posted')
    related_sale                  = fields.Many2one('facturas.sales_ventas', string="Presupuesto de venta relacionado", readonly=True)
    has_related_albaran           = fields.Boolean(compute='_compute_has_related_albaran', string="Tiene albarán relacionado", store=True)
    related_albaran_count         = fields.Integer(compute='_compute_has_related_albaran', string='Albaránes relacionados', store=True)
    related_albaran_ids           = fields.One2many('facturas.albaranes', 'related_compra', string="Compras relacionadas")
    payment_term_id               = fields.Many2one('account.payment.term', string='Plazo de pago', readonly=False)
    x_notes_purchase_agency       = fields.Text(string='Notas de compra')

    


    def write(self, vals):
        # Verificar si el estado cambia a 'confirmed'
        if 'status' in vals and vals['status'] == 'confirmed':
            for record in self:
                existing_record = False
                # Comprobar si el numero_pedido_cliente no está vacío
                if record.numero_pedido_cliente:
                    # Comprobar si ya existe un registro en facturas.albaranes con el mismo número de pedido de cliente
                    existing_record = self.env['facturas.albaranes'].search([('numero_pedido_cliente', '=', record.numero_pedido_cliente)], limit=1)

                # Si no existe, crear uno nuevo
                if not existing_record:
                    new_albaran = self.env['facturas.albaranes'].create({
                        'numero_pedido_cliente': record.numero_pedido_cliente,
                        'status': 'posted',
                        'customer': record.customer.id,
                        'direccion_entrega': record.direccion_entrega.id,
                        'fecha_entrega': record.fecha_entrega,
                        'fecha_confirmacion': record.fecha_confirmacion,
                        'numero_confirmacion_fabrica': record.numero_confirmacion_fabrica,
                        'supplier_id': record.supplier_id.id,
                        'amount_untaxed': record.amount_untaxed,
                        'amount_tax': record.amount_tax,
                        'amount_total': record.amount_total,
                        'currency_id': record.currency_id.id,
                        'observaciones': record.observaciones,
                        'related_compra': record.id,
                        'x_notes_delivery_agency': record.customer.x_notes_delivery_agency
                        # ... (agregar aquí el resto de los campos que desees copiar o establecer)
                    })
                    for line in record.sales_compras_line_ids:
                        new_line_values = {
                            'albaranes_id': new_albaran.id,
                            'customer_id': line.customer_id.id,
                            'product_id': line.product_id.id,
                            'gramo_metro': line.gramo_metro,
                            'ancho': line.ancho,
                            'cantidad': line.cantidad,
                            'precio': line.precio,
                            'fecha_entrega': line.fecha_entrega,
                            'mand': line.mand,
                            'diametro': line.diametro,
                            'discount': line.discount,
                            'tax_id': [(6, 0, line.tax_id.ids)],
                        }
                        self.env['facturas.albaranes.line'].create(new_line_values)
        return super(sales_compras, self).write(vals)

    @api.depends('related_albaran_ids')
    def _compute_has_related_albaran(self):
        for record in self:
            record.has_related_albaran = bool(record.related_albaran_ids)
            record.related_albaran_count = len(record.related_albaran_ids)
       

    def action_related_albaran(self):
        self.ensure_one()
        purchases = self.env['facturas.albaranes'].search([('related_compra', '=', self.id)])

        return {
            'name': 'Albaranes relacionados',
            'type': 'ir.actions.act_window',
            'res_model': 'facturas.albaranes',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', purchases.ids)],
            'context': {'default_related_albaran': self.id},
            'target': 'current',
        }

    _sql_constraints = [
        ('unique_numero_pedido_cliente', 'unique(numero_pedido_cliente)', ('El número de pedido ya está asignada a otro registro.')),
    ]

    def action_toggle_archive(self):
        if self.status == 'archived':
            self.status = 'draft'
            
            
        else:
            self.status = 'archived'
            
    
    def action_toggle_confirm(self):
        if self.status == 'confirmed':
            self.status = 'draft'
            
            
        else:
            # Comprueba si la fecha de entrega confirmada está establecida
           

            # Si tiene un presupuesto de venta asociado, actualiza su fecha de entrega confirmada y el número de pedido de fábrica
            if self.related_sale:
                existing_record = self.env['facturas.sales_ventas'].search([('id', '=', self.related_sale.id)], limit=1)
                existing_record.write({'fecha_confirmacion': self.fecha_confirmacion, 'numero_confirmacion_fabrica':self.numero_confirmacion_fabrica})
                self.status = 'confirmed'
            else:
                self.status = 'confirmed'

    @api.onchange('customer')
    def _onchange_customer(self):
        if self.customer:
            self.direccion_entrega         = self.customer
            self.payment_term_id           = self.customer.property_supplier_payment_term_id
            self.x_notes_purchase_agency   = self.customer.x_notes_purchase_agency
            
        else:
            self.direccion_entrega         = False
            self.payment_term_id           = False
            self.x_notes_purchase_agency   = False

    @api.depends('sales_compras_line_ids.price_subtotal', 'sales_compras_line_ids.tax_id', 'sales_compras_line_ids.cantidad', 'sales_compras_line_ids.precio', 'sales_compras_line_ids.discount')
    def _compute_amount(self):
        for sale in self:
            amount_untaxed = 0.0
            amount_tax = 0.0
            for line in sale.sales_compras_line_ids:
                amount_untaxed += line.price_subtotal
                taxes = line.tax_id.compute_all(line.precio * (1 - (line.discount or 0.0) / 100.0), quantity=line.cantidad)
                amount_tax += sum(tax.get('amount', 0.0) for tax in taxes.get('taxes', []))
            sale.amount_untaxed = amount_untaxed
            sale.amount_tax = amount_tax
            sale.amount_total = amount_untaxed + amount_tax
    
    @api.model
    def create(self, vals):
        if not vals.get('sequence'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('facturas.sales_compras') or 0
        
        return super(sales_compras, self).create(vals)
    
    @api.constrains('sequence')
    def _check_unique_sequence(self):
        for record in self:
            if self.env['facturas.sales_compras'].search_count([('sequence', '=', record.sequence)]) > 1:
                raise ValidationError('El número de presupuesto debe ser único.')

    @api.onchange('fecha_entrega_confirmada')
    def _onchange_fecha_entrega_confirmada(self):
        # Si tiene un presupuesto de venta asociado, actualiza su fecha de entrega confirmada
        if self.related_sale:
            self.related_sale.fecha_entrega_confirmada = self.fecha_entrega_confirmada


class PresupuestosSaleLine(models.Model):
    _name = 'facturas.sales_compras.line'
    _description = 'Línea de Presupuesto'

    
    sales_compras_id      = fields.Many2one('facturas.sales_compras', string='Presupuesto')
    customer_id           = fields.Many2one('res.partner', related='sales_compras_id.customer', string='Cliente', readonly=True)
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