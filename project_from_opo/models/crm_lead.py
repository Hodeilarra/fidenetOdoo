from odoo import models, api

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def create(self, vals):
        record = super(CRMLead, self).create(vals)
        if record.type == 'opportunity' and record.stage_id.is_won:
            self._create_project_for_opportunity(record)
        return record

    def write(self, vals):
        res = super(CRMLead, self).write(vals)
        for record in self:
            if record.type == 'opportunity' and record.stage_id.is_won:
                if not self.env['project.project'].search([('opportunity_id', '=', record.id)], limit=1):
                    self._create_project_for_opportunity(record)
        return res

    def _create_project_for_opportunity(self, opportunity):
        self.env['project.project'].create({
            'name': opportunity.name,
            'partner_id': opportunity.partner_id.id,
          
            'opportunity_id': opportunity.id,
        })