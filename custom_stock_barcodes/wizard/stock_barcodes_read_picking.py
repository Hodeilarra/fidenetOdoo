# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.tools.float_utils import float_compare


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    def _process_stock_move_line(self):
        """
        Search assigned or confirmed stock moves from a picking operation type
        or a picking. If there is more than one picking with demand from
        scanned product the interface allow to select what picking to work.
        If only there is one picking the scan data is assigned to it.
        """
        StockMove = self.env["stock.move"]
        StockMoveLine = self.env["stock.move.line"]
        moves_todo = StockMove.search(self._prepare_stock_moves_domain())
        if not self._search_candidate_picking(moves_todo):
            return False
        if not self.allow_duplicated and\
                self.picking_id.move_line_ids_without_package.filtered(lambda x: x.lot_id.id == self.lot_id.id
                                                                       and x.qty_done > 0):
            """
            Quitamos el control de lecturas del historial mientras nos vale con que no esté en los move_line_ids_without_package
            or self.scan_log_ids.filtered(lambda x: x.lot_id.id == self.lot_id.id)):"""
            self._set_messagge_info(
                "info", _("This S/N or Lot id has been already scanned, remove ir from the scanned lines")
            )
            # Sonido ERROR
            self.play_sounds(False)
            return False
        """190822: Quieren que la reserva de los lotes se haga en el momento de la salida del material
        Piso el método completo: Busco el producto por picking, producto, cantidad y estado
        Además añado en el wirte (linea+-43) el lot_id para que lo deje reservado para el move_line"""
        #  Buscamos si el lote scaneado está reservado en otro sitio
        #  Si está reservado lo liberamos y lo intercambiamos por otro reservado picking actual
        if self.picking_id.picking_type_id.code != 'incomming':
            lines = self._sn_reserve_control()
        else:
            lines = moves_todo.mapped("move_line_ids").filtered(
            lambda l: (
                l.picking_id == self.picking_id
                and l.product_id == self.product_id
                # and l.lot_id == self.lot_id
                and l.qty_done < self.product_qty
                and l.state in self._states_move_allowed()

            )
        )

        available_qty = self.product_qty
        move_lines_dic = {}
        for line in lines:
            if line.product_uom_qty:
                assigned_qty = min(
                    max(line.product_uom_qty - line.qty_done, 0.0), available_qty
                )
            else:
                assigned_qty = available_qty
            line.write({"qty_done": line.qty_done + assigned_qty,
                        "lot_id": self.lot_id.id})
            available_qty -= assigned_qty
            if assigned_qty:
                move_lines_dic[line.id] = assigned_qty
            if (
                float_compare(
                    available_qty,
                    0.0,
                    precision_rounding=line.product_id.uom_id.rounding,
                )
                < 1
            ):
                break
        if (
            float_compare(
                available_qty, 0, precision_rounding=self.product_id.uom_id.rounding
            )
            > 0
        ):
            # Create an extra stock move line if this product has an
            # initial demand.
            moves = self.picking_id.move_lines.filtered(
                lambda m: (
                    m.product_id == self.product_id
                    and m.state in self._states_move_allowed()
                )
            )
            if not moves:
                # TODO: Add picking if picking_id to message
                self._set_messagge_info(
                    "info", _("There are no stock moves to assign this operation")
                )
                # Sonido ERROR
                self.play_sounds(False)
                return False
            else:
                line = StockMoveLine.create(
                    self._prepare_move_line_values(moves[0], available_qty)
                )
                move_lines_dic[line.id] = available_qty
        self.picking_product_qty = sum(moves_todo.mapped("quantity_done"))
        return move_lines_dic

    def _sn_reserve_control(self):
        # Buscamos una reserva del picking del producto SIN lot_name
        reserved_curr_pick_prod = self._search_move_line_reserved(picking=self.picking_id, current_lot=False)
        # Si no hay nada reservado paramos
        if not reserved_curr_pick_prod:
            return reserved_curr_pick_prod
        # Buscamos en el picking actual que coincida lot_name
        reserved_curr_pick = self._search_move_line_reserved(picking=self.picking_id)
        # Si está reservado no hace falta buscar más
        if reserved_curr_pick:
            return reserved_curr_pick
        # Buscanos reservas del lot_name en otros picks
        reserved_other_pick = self._search_move_line_reserved(exclude_picking=self.picking_id, check_done=False)

        if reserved_other_pick:
            # Si existen intecarbiamos reservas
            if reserved_other_pick.qty_done < self.product_qty:
                cur_pick = reserved_curr_pick_prod.picking_id
                cur_move = reserved_curr_pick_prod.move_id
                reserved_curr_pick_prod.picking_id = reserved_other_pick.picking_id
                reserved_curr_pick_prod.move_id = reserved_other_pick.move_id
                reserved_other_pick.picking_id = cur_pick
                reserved_other_pick.move_id = cur_move
                return reserved_other_pick
            # este caso es que está reservado en otro albarán con las unidades realizadas
            return []
        # Devolvemos la reserva de producto
        return reserved_curr_pick_prod


    def _search_move_line_reserved(self, picking=False, exclude_picking=False, current_lot=True, check_done=True):
        search_domain = [
                ('product_id', "=", self.product_id.id),
                ('state', "in", self._states_move_allowed()),
             ]
        if check_done:
            search_domain.append(('qty_done', "<", self.product_qty))
        if current_lot:
            search_domain.append(('lot_id', "=", self.lot_id.id))
        if picking:
            search_domain.append(('picking_id', '=', picking.id))
        if exclude_picking:
            search_domain.append(('picking_id', '!=', exclude_picking.id))
        lines = self.env['stock.move.line'].search(search_domain)
        return lines[:1]

    def _states_move_allowed(self):
        ret = super()._states_move_allowed()
        ret.append('partially_available')
        return ret
