# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('draft', 'Pendiente'),
                                             ('sent', 'Enviado'),
                                             ('sale', 'Aceptado'),
                                             ('done', 'Bloqueado'),
                                             ('cancel', 'Cancelado')])