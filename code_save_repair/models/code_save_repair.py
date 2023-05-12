from odoo import models, fields, api

class CodeSaveRepair(models.Model):
    _inherit = 'repair.view_repair_order_form'

    print('*****************************************AAA*************************************************')

    @api.model
    def write(self, vals):
        print('*************************************************Guardando datos*************************************************')
        override_write  = super(CodeSaveRepair, self).write(vals)
        print('*************************************************Guardando datos*************************************************')
        return override_write