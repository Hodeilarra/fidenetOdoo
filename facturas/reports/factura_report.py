# reports/factura_report.py
from odoo import api, models

class FacturaReport(models.AbstractModel):
    _name = 'report.facturas.factura_report_template'
    _description = 'Factura Report'

    #@api.model
    #def _get_report_values(self, docids, data=None):
    #    docs = self.env['facturas.invoice'].browse(docids)
    #    return {
    #        'doc_ids': docids,
    #        'doc_model': 'facturas.invoice',
    #        'docs': docs,
    #    }

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['facturas.invoice'].browse(docids)
        # Recopilar información de las líneas de factura para cada factura
       
        return {
            'doc_ids': docids,
            'doc_model': 'facturas.invoice',
            'docs': docs,
            
        }