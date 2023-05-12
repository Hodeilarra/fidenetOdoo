# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state_invoice = fields.Selection(selection_add=[('returned', 'Devuelto')])

    def write(self, vals):
        if 'date_done' in vals:
            returned_moves_from_so = self.move_ids_without_package.mapped(
                'origin_returned_move_id').mapped('sale_line_id')
            if returned_moves_from_so:
                vals['state_invoice'] = 'returned'
        res = super().write(vals)
        return res


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        res = super()._create_returns()
        # Comprobamos si está todo devuelto y si es verdad lo ponemos en estado 'returned'
        returned = self.env['stock.move'].search([('origin_returned_move_id', 'in', self.picking_id.move_lines.ids)])
        if len(returned) == len(self.picking_id.move_lines):
            self.picking_id.state_invoice = 'returned'
        return res

