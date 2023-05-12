from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_view_sale_order(self):
        print("***********************************************SALEEEEEE***********************************************")
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.pop("default_picking_id", False)
        return self.with_context(ctx).sale_id.get_formview_action()

    def action_view_purchase_order(self):
        print("***********************************************PURCHASEEE***********************************************")
        self.ensure_one()
        xmlid = "purchase.purchase_form_action"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        form = self.env.ref("purchase.purchase_order_form")
        action["views"] = [(form.id, "form")]
        action["res_id"] = self.purchase_id.id
        return action
