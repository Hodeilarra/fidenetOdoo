# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class RepairLineDiscount(models.Model):
    _inherit = 'repair.line'
    discount            = fields.Float(string='Descuento (%)', default=0.0)
    product_price       = fields.Float(related='product_id.lst_price', string='Precio del Producto', readonly=True)
    price_subtotal      = fields.Monetary(compute='_compute_price_subtotal', string='Subtotal', store=True)
    amount_total        = fields.Monetary(compute='_compute_price_subtotal', string='Total', store=True)
    amount_tax          = fields.Float(compute='_compute_price_subtotal', string='Tax', store=True)
   
    @api.onchange('product_uom_qty', 'discount', 'price_unit')
    def _onchange_calculate_discount_and_taxes(self):
        if self.discount:
            self.price_unit = self.price_unit * (1 - (self.discount / 100))

        # Una vez aplicado el descuento, los impuestos se calcularán automáticamente basándose en el price_unit actualizado
        # Suponiendo que los impuestos ya están configurados correctamente en el producto
        




    
    