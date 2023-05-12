from odoo import fields, models, api

class CustomGeneralLedgerReportWizard(models.TransientModel):
    _inherit = "general.ledger.report.wizard"

    account_ids_count = fields.Integer(
        string="Cantidad de cuentas", compute="_compute_account_ids_count"
    )

    @api.depends("account_ids")
    def _compute_account_ids_count(self):
        for record in self:
            record.account_ids_count = len(record.account_ids)