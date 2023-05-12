from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.constrains('sanitized_acc_number', 'partner_id', 'company_id')
    def _check_unique_number(self):
        if not self.env.context.get('ignore_unique_number_constraint', False):
            existing_bank_accounts = self.search_count([
                ('sanitized_acc_number', '=', self.sanitized_acc_number),
                ('company_id', '=', self.company_id.id),
                ('partner_id', '=', self.partner_id.id),
            ])
            if existing_bank_accounts > 1:
                raise ValidationError('Account Number must be unique')

    _sql_constraints = [
        ('unique_number', 'unique(sanitized_acc_number, company_id, partner_id)', 'Account Number must be unique'),
    ]

    #def _sql_drop(self):
    #    cr = self.env.cr
    #    cr.execute("ALTER TABLE res_partner_bank DROP CONSTRAINT IF EXISTS 	res_partner_bank_unique_number")