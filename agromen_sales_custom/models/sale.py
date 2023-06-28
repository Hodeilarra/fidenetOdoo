from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Pendiente'),   # Cambiaste 'Draft Quotation' a 'Presupuesto'
        ('sent', 'Quotation Sent'),
        ('sale', 'Aceptado'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    fecha_envio = fields.Datetime(string='Fecha de Envío')
    obra_asociada = fields.Many2one('project.project', string='Obra Asociada')
    project_id = fields.Many2one('project.project')
    
    administrador_finca = fields.Many2one('res.partner', string='Administrador de finca')

    comercial_obra = fields.Many2one('res.partner', string='Comercial de obra')

    variant_number = fields.Integer(default=0, copy=False)
    variant_count = fields.Integer('Variant Count', default=0, compute='_compute_variant_count')
    is_variant = fields.Boolean(default=False, copy=False)

    def action_archive(self):
        """ Archivar los registros seleccionados """
        self.write({'active': False})
        return True
    
    def _compute_variant_count(self):
        for record in self:
            record.variant_count = self.env['sale.order'].search_count([
                ('name', 'like', record.name+'-%'),
                ('is_variant', '=', True)
            ])


    #CON LINEAS DE PEDIDO Y TOTALES:
    #def create_variant(self):
    #    self.ensure_one()
    #    if not self.is_variant:
    #        new_order = self.copy({
    #            'name': '{}-{:02d}'.format(self.name, self.variant_count + 1),
    #            'variant_number': self.variant_count + 1,
    #            'is_variant': True,
    #        })
    #        self.variant_count += 1
    #        return {
    #            'type': 'ir.actions.act_window',
    #            'res_model': 'sale.order',
    #            'view_mode': 'form',
    #            'res_id': new_order.id,
    #        }
    #    else:
    #        raise UserError(_('No puedes crear una variante de otra variante.'))

    
    #SIN LINEAS DE PEDIDO NI TOTALES:
    
    def create_variant(self):
        self.ensure_one()
        if not self.is_variant:
            new_order = self.copy({
                'name': '{}-{:02d}'.format(self.name, self.variant_count + 1),
                'variant_number': self.variant_count + 1,
                'is_variant': True,
                'order_line': False,  # This clears the order lines
                'amount_total': 0,
                'amount_untaxed': 0,
                'amount_tax': 0,
            })
            self.variant_count += 1
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': new_order.id,
            }
        else:
            raise UserError(_('No puedes crear una variante de otra variante.'))



    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            if not order.is_variant:  # Asegúrate de que 'is_variant' es un atributo de 'order'
                try:
                    project = self.env['project.project'].create({
                        'name': order.name,
                        'partner_id': order.partner_id.id,
                        'presupuesto_asociado': order.id,
                    })

                    # Asignar el proyecto al pedido
                    order.obra_asociada = project

                    # Crear el mensaje de usuario
                    order.message_post(body=_('Se ha creado un nuevo proyecto: %s') % project.name)
                except Exception as e:
                    _logger.exception("Error al crear el proyecto: %s", e)
        return res


    def write(self, vals):
        if 'state' in vals and vals['state'] == 'sent':
            vals['fecha_envio'] = fields.Datetime.now()
        return super(SaleOrder, self).write(vals)

