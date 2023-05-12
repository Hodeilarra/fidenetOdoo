from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
class invoice(models.Model):
    _name = 'facturas.invoice'
    _description = 'Allows you to define the characteristics of an invoice'
    _rec_name = 'sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    sequence                        = fields.Char(string='Número', readonly=True, copy=False, default='/')
    customer                        = fields.Many2one('res.partner', string='Cliente', required=True)
    product_id                      = fields.Many2one('product.product', string='Producto')
    invoice_date                    = fields.Date('Fecha de factura',default=fields.Date.context_today)
    invoice_date_due                = fields.Date('Fecha de vencimiento')
    comision                        = fields.Selection([('5', '5%'), ('3', '3%'), ('2', '2%'), ('1.5', '1.5%')],string='Comisión %')
    total_comision                  = fields.Float('Total comisión (€)', required=True, compute='_compute_amount')
    price                           = fields.Monetary(currency_field='currency_id', string='Precio')
    status                          = fields.Selection([('draft', 'Borrador'),('confirmed', 'Confirmado'),('posted', 'Publicado'),('cancel', 'Cancelado'),('pending', 'Pendiente de pago'),('archived', 'Archivado')], string='Estado', default='posted')
    payment_state                   = fields.Selection([('not_paid', 'No pagadas'),('in_payment', 'En proceso de pago'),('paid', 'Pagado'),('partial', 'Pagado Parcialmente'),('reversed', 'Revertido'),('facturas_legacy','Factura sistema anterior')], string='Estado de pago', default='not_paid')
    invoice_line_ids                = fields.One2many('facturas.invoice.line', 'invoice_id', string='Líneas de Factura')
    amount_untaxed                  = fields.Monetary(string='Base imponible', currency_field='currency_id', compute='_compute_amount')
    amount_tax                      = fields.Float(string='Impuestos', compute='_compute_amount')
    amount_total                    = fields.Float(string='Total', compute='_compute_amount')
    active                          = fields.Boolean(string='Activo', default=True)
    currency_id                     = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    archive_button                  = fields.Char(string='Archivar', type='object')
    supplier_id                     = fields.Many2one('res.partner',string='Proveedor', domain=[('supplier_rank', '>', 0)],help='Selecciona un proveedor')
    invoice_id                      = fields.Char(string='Número de factura',help='Selecciona una factura')
    factory_order_number            = fields.Char(string='Número de pedido de fábrica',help='Introduce el número de pedido de fábrica')
    customer_order_number           = fields.Char(string='Número de pedido de cliente',help='Introduce el número de pedido de cliente')
    related_document                = fields.Reference(selection=[('facturas.albaranes', 'Albarán'), ('facturas.sales_ventas', 'Presupuesto de venta')],string='Documento asociado',)
    payment_term_id                 = fields.Many2one('account.payment.term', string='Plazo de pago', readonly=False)
    days                            = fields.Integer(string='Días', default=0)
    company_id                      = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)
    x_notes_invoice_agency          = fields.Text(string='Notas de factura de agencia')
    
    #@api.onchange('customer', 'invoice_date')
    #def _onchange_customer_or_invoice_date(self):
    #    self._update_invoice_date_due()



    def create_invoice_by_supplier(self, selected_invoice_ids):
        grouped_invoices = {}
        for invoice_id in selected_invoice_ids:
            invoice = self.env['facturas.invoice'].browse(invoice_id)
            if invoice.supplier_id.id not in grouped_invoices:
                grouped_invoices[invoice.supplier_id.id] = []
            grouped_invoices[invoice.supplier_id.id].append(invoice)

        commission_product = self.env['product.product'].search([('name', '=', 'Comisión')], limit=1)
        if not commission_product:
            raise UserError(_("No se encuentra el producto 'Comisión'. Por favor, asegúrese de que existe."))

        for supplier_id, invoices in grouped_invoices.items():
            supplier = self.env['res.partner'].browse(supplier_id)
            total_amount = sum(invoice.total_comision for invoice in invoices)

            origin_docs = ', '.join([inv.display_name for inv in invoices])

            # Crear una factura de cliente de Odoo (account.move)
            account_move = self.env['account.move'].create({
                'partner_id': supplier.id,
                'move_type': 'out_invoice',  # Factura de cliente
                'invoice_date_due': False,
                'invoice_line_ids': [(0, 0, {
                    'name': 'Factura consolidada - Documentos de origen: {}'.format(origin_docs),
                    'product_id': commission_product.id,
                    'quantity': 1,
                    'price_unit': total_amount,
                    'tax_ids': [(6, 0, commission_product.taxes_id.ids)],
                })],
            })

            # Agregar enlaces a las facturas originales en la factura de Odoo
            for invoice in invoices:
                self.env['account.move.origin'].create({
                    'move_id': account_move.id,
                    'origin_id': invoice.id,
                    'origin_model': 'facturas.invoice',
                })

    
    def create_invoice_by_supplier_action(self):
        selected_invoice_ids = self.env.context.get('active_ids', [])
        self.create_invoice_by_supplier(selected_invoice_ids)

    def _update_invoice_date_due(self):
        if self.invoice_date and self.days:
            invoice_date = fields.Date.from_string(self.invoice_date)
            due_date = invoice_date + timedelta(days=self.days)
            self.invoice_date_due = fields.Date.to_string(due_date)
            
        

    @api.onchange('customer', 'invoice_date')
    def _onchange_customer(self):
        if self.customer:
            self.payment_term_id   = self.customer.property_supplier_payment_term_id
            self._update_invoice_date_due()
        else:
            self.payment_term_id   = False

    @api.onchange('customer')
    def _onchange_customer2(self):
        if self.customer:
            self.x_notes_invoice_agency   = self.customer.x_notes_invoice_agency
          
        else:
            self.x_notes_invoice_agency   = False

    @api.onchange('payment_term_id')
    def _onchange_payment_term_id(self):
        self._update_invoice_date_due()

    def _update_invoice_date_due(self):
        if self.invoice_date and self.payment_term_id:
            payment_term = self.payment_term_id
            due_date = False
            for line in payment_term.line_ids:
                days = line.days
                invoice_date = fields.Date.from_string(self.invoice_date)
                new_due_date = invoice_date + timedelta(days=days)
                if not due_date or new_due_date > due_date:
                    due_date = new_due_date
            self.invoice_date_due = fields.Date.to_string(due_date)
        else:
            self.invoice_date_due = False
    
    @api.constrains('customer_order_number')
    def _check_unique_customer_order_number(self):
        for record in self:
            # Comprobar si el customer_order_number no está vacío
            if record.customer_order_number:
                if self.env['facturas.invoice'].search_count([('customer_order_number', '=', record.customer_order_number), ('id', '!=', record.id)]) > 0:
                    raise ValidationError('Ya existe una factura con el mismo Número de pedido de cliente.')
    
    # Restricción SQL para garantizar la unicidad del campo invoice_id
    _sql_constraints = [
        ('unique_invoice_id', 'unique(invoice_id)', ('La factura ya está asignada a otro registro.')),
    ]

    

    def action_toggle_archive(self):
        if self.status == 'archived':
            self.status = 'draft'
            
            
        else:
            self.status = 'archived'
            
    def action_quotation_send(self):
        template = self.env.ref('facturas.invoice_mail_template') # referencia a la plantilla de correo electrónico
        template.send_mail(self.id, force_send=True)
    
    def action_toggle_confirm(self):
        if self.status == 'confirmed':
            self.status = 'draft'
            
            
        else:
            self.status = 'confirmed'
            
    
    

    @api.model
    def create(self, vals):
        if not vals.get('sequence'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('facturas.invoice') or 0
        self.status = "posted"
        return super(invoice, self).create(vals)
    
    @api.constrains('sequence')
    def _check_unique_sequence(self):
        for record in self:
            if self.env['facturas.invoice'].search_count([('sequence', '=', record.sequence)]) > 1:
                raise ValidationError('El número de factura debe ser único.')


    @api.depends('invoice_line_ids.price_subtotal', 'invoice_line_ids.tax_id', 'invoice_line_ids.quantity', 'invoice_line_ids.price_unit', 'invoice_line_ids.discount', 'comision')
    def _compute_amount(self):
        for invoice in self:
            amount_untaxed = 0.0
            amount_tax = 0.0
            for line in invoice.invoice_line_ids:
                amount_untaxed += line.price_subtotal
                taxes = line.tax_id.compute_all(line.price_unit * (1 - (line.discount or 0.0) / 100.0), quantity=line.quantity)
                amount_tax += sum(tax.get('amount', 0.0) for tax in taxes.get('taxes', []))
            invoice.amount_untaxed = amount_untaxed
            invoice.amount_tax = amount_tax
            invoice.amount_total = amount_untaxed + amount_tax
            if invoice.comision == 0:
                
                invoice.total_comision = 0
            else:
                
                invoice.total_comision = (float(invoice.comision) * invoice.amount_untaxed) / 100.0
            

class FacturasInvoiceLine(models.Model):
    _name = 'facturas.invoice.line'
    _description = 'Línea de Factura'

   
    invoice_id            = fields.Many2one('facturas.invoice', string='Factura')
    customer_id           = fields.Many2one('res.partner', related='invoice_id.customer', string='Cliente', readonly=True)    
    product_id            = fields.Many2one('product.product', string='Producto')
    quantity              = fields.Float(string='Cantidad (kgs)', default=1.0)
    price_unit            = fields.Float(string='Precio (€/kg)', required=True)
    discount              = fields.Float(string='Descuento (%)')
    tax_id                = fields.Many2many('account.tax', string='Impuestos')
    price_subtotal        = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    gramo_metro           = fields.Float(readonly=True, string='g/m²')
    ancho                 = fields.Float(string='Ancho (mm)', default=1.0)
    mand                  = fields.Float(related='customer_id.mand', string='Mand. (mm)', readonly=False)
    diametro              = fields.Float(related='customer_id.diametro', string='Diam.Ex. (cm)', readonly=False)

    @api.depends('quantity', 'price_unit', 'discount')
    def _compute_subtotal(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.price_subtotal = price * line.quantity

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
        else:
            self.price_unit = 0.0


class AccountMoveOrigin(models.Model):
    _name = 'account.move.origin'
    _description = 'Factura de Origen'

    move_id             = fields.Many2one('account.move', 'Factura de Odoo', required=True, ondelete='cascade')
    origin_id           = fields.Many2one('facturas.invoice', 'Factura de Origen', required=True, ondelete='cascade')
    origin_model        = fields.Char('Modelo de Origen', required=True)
    origin_name         = fields.Char(related='origin_id.display_name', string='Nombre de Factura', readonly=True)
    related_invoice_id  = fields.Char(related='origin_id.invoice_id', string='Número de factura', readonly=True)
            

class AccountMove(models.Model):
    _inherit = 'account.move'

    origin_ids = fields.One2many('account.move.origin', 'move_id', string='Documentos de Origen')
    