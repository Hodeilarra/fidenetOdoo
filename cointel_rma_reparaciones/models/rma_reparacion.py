# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class Rma_Reparacion(models.Model):
    _inherit = "rma"

    reparacion = fields.Many2one('repair.order', string="Reparación")

    estado_reparacion = fields.Selection(related='reparacion.state', string="Estado Reparación")

    picking_id = fields.Many2one('stock.picking', string="Origin Delivery")

    seleccion_producto = fields.Many2one('selection.selection', string="Seleccion Producto", domain="[('picking','=',picking_id)]")

    move_id = fields.Many2one("stock.move", string="Origin move",)

    @api.onchange('picking_id')
    def onchange_picking_id(self):
        busqueda = self.env['selection.selection'].search([('picking', '=', self.picking_id.id)])
        if(len(busqueda) == 0):
            for lineaProducto in self.picking_id.move_line_ids_without_package:
                if(lineaProducto.lot_id):
                    self.env['selection.selection'].create({
                    'name': lineaProducto.display_name+" "+lineaProducto.lot_id.display_name,
                    'value': lineaProducto.display_name+" "+lineaProducto.lot_id.display_name,
                    'picking': self.picking_id.id
                    })
                else:
                    self.env['selection.selection'].create({
                    'name': lineaProducto.display_name,
                    'value': lineaProducto.display_name,
                    'picking': self.picking_id.id
                    })

    @api.onchange('seleccion_producto')
    def onchange_seleccion_producto_id(self):
        busqueda = self.env['stock.move'].search([('picking_id', '=', self.picking_id.id)])
        for move in busqueda:
            if(str(move.product_id.display_name) in str(self.seleccion_producto.display_name)):
                self.move_id = move
    
    def action_confirm(self):
        overwrite = super(Rma_Reparacion, self).action_confirm()
        lotes = self.env['stock.production.lot'].search([('product_id.name', '=', self.reception_move_id.name)])
        if(self.seleccion_producto.display_name):
            loteSeleccionado = self.seleccion_producto.display_name.split(" ")
            for lote in lotes:
                if(loteSeleccionado[1] == lote.display_name):
                    numeroSerieSeleccionado = lote
                    self.reception_move_id.lot_ids = numeroSerieSeleccionado
        

class selection_selection(models.Model):
    _name = 'selection.selection'
    
    picking = fields.Many2one('Picking', required=True)
    name = fields.Char('Name', required=True)
    value = fields.Char('Value', required=True)