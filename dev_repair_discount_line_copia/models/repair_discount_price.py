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

class RepairOrder(models.Model):
    _inherit = 'repair.order'
    @api.depends('order_line.price_reduce', 'order_line.tax_id', 'order_line.product_uom_qty')
    def _compute_repair_tax(self):
        for order in self:
            tax_ids = order.order_line.mapped('tax_id')
            taxes = tax_ids.compute_all(
                order.order_line.price_reduce,
                quantity=order.order_line.product_uom_qty,
                product=order.order_line.product_id,
                partner=order.partner_id
            )
            order.update({
                'amount_untaxed': taxes['total_excluded'],
                'amount_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'amount_total': taxes['total_included'],
            })

    class RepairLine(models.Model):
        _inherit = 'repair.line'
        
        discount = fields.Float(string='Descuento (%)', default=0.0)
        price_reduce = fields.Monetary(compute='_compute_price_reduce', string='Precio con descuento')
        
        @api.depends('price_unit', 'discount')
        def _compute_price_reduce(self):
            for line in self:
                if line.discount > 100:
                    raise ValueError("El descuento no puede ser mayor que el 100%.")
                line.price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
        
        