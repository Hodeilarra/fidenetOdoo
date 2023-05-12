# reports/factura_report.py
from odoo import api, models

class CompraReport(models.AbstractModel):
    _name = 'report.facturas.albaran_report_template'
    _description = 'Albarán Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['facturas.albaranes'].browse(docids)
        # Recopilar información de las líneas de factura para cada factura
       
        return {
            'doc_ids': docids,
            'doc_model': 'facturas.albaranes',
            'docs': docs,
            
        }