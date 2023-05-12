from odoo import _, api, exceptions, fields, models, tools


class UrlSourceCOde(models.Model):
    _inherit = "stock.picking"

    hide = fields.Boolean(string="Hide", compute="_set_hide", store=False)
    hidep = fields.Boolean(string="Hidep", compute="_set_hidep", store=False)

    @api.depends('sale_id')
    def _set_hide(self):
        if self.sale_id.id:
            self.hide = False
        else:
            self.hide = True
    
    @api.depends('purchase_id')
    def _set_hidep(self):
        if self.purchase_id.id:
            self.hidep = False
        else:
            self.hidep = True

    def action_view_sale_order(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.pop("default_picking_id", False)
        return self.with_context(ctx).sale_id.get_formview_action()

    def action_view_purchase_order(self):
        self.ensure_one()
        xmlid = "purchase.purchase_form_action"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        form = self.env.ref("purchase.purchase_order_form")
        action["views"] = [(form.id, "form")]
        action["res_id"] = self.purchase_id.id
        return action
