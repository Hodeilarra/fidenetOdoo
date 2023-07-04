from odoo import api, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('user_id')
    def _check_user_id(self):
        group_own_orders = self.env.ref('purchase_security.group_purchase_own_orders')
        group_manager = self.env.ref('purchase.group_purchase_manager')
        if group_own_orders in self.env.user.groups_id and self.user_id and self.user_id != self.env.user and group_manager not in self.env.user.groups_id:
            raise UserError(_('Con los permisos que tienes solo puedes elegirte a ti mismo o dejar el campo vacío.'))