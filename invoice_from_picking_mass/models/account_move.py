# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    invoicefrompicking_id = fields.Many2one('invoice.from.picking.mass', 'Facturado desde', copy=False)
    picking_id = fields.Many2one('stock.picking', 'Albarán', copy=False)
    picking_origin = fields.Char('Picking Origin', compute='_giveme_origin', copy=False)


    def _giveme_origin(self):
        for record in self:
            picking_origin = ""
            if record.invoicefrompicking_id:
                for line in record.invoicefrompicking_id.invoicefrompicking_line_ids:
                    picking_origin += line.picking_id.name + ", "
            else:
                picking_origin = '-'

            record.picking_origin = picking_origin[:-2]



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    picking_id = fields.Many2one('stock.picking', 'Albarán')
    line_picking_id = fields.Many2one('stock.move', 'Linea Albarán')