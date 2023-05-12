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
   
    @api.depends('discount','price_unit','product_uom_qty')
    def _compute_price_subtotal(self):
        print("Precio del producto:"+str(self.price_unit))
        for line in self:
            if line.discount > 100:
                raise ValidationError(_("El descuento debe ser menor que el 100%"))
            else:
                #line.price_unit = line.product_price
                 
                line.price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                #line.price_unit = precio_descontado
                taxes = line.tax_id.compute_all(line.price_unit, line.repair_id.currency_id, line.product_uom_qty, product=line.product_id)
                line.update({
                    'amount_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'amount_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })





    
    