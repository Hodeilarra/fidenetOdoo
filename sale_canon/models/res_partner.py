from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    canon_excluded = fields.Boolean()

    def _get_client_is_excluded(self):
        self.ensure_one()
        self._onchange_country_id()
        return self.canon_excluded

    @api.onchange("country_id")
    def _onchange_country_id(self):
        spain = self.env.ref("base.es")
        if not self.canon_excluded:
            if self.country_id and self.country_id != spain:
                self.canon_excluded = True
            else:
                self.canon_excluded = False
