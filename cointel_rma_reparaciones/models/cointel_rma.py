# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class Cointel_Rma(models.Model):
    _inherit = "stock.picking"

    valorBoton = fields.Boolean(string="ValorBoton", compute="_set_valorBoton", store=False)

    @api.depends('state')
    def _set_valorBoton(self):
        valorEstado = dict(self._fields['state'].selection).get(self.state)
        if (valorEstado == "Done"):
            self.valorBoton = False
        else:
            self.valorBoton = True

    def repair_order_custom(self):
        nombre = self.origin.split(' ')
        rma = self.env['rma'].search([('name', '=', nombre[0])])
        for linea in self.move_line_ids:
            repair = self.env['repair.order'].create({
			'product_id': linea.product_id.id,
            'product_uom': linea.product_id.uom_id.id,
            'lot_id': linea.lot_id.id,
            'location_id': 18, # RMAko biltegie apuntau
			'partner_id': self.partner_id.id,
            'rma': rma.id,
            'state' : "borrador"
		    })
        rma.reparacion = repair.id
        return self