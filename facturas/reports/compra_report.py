# reports/factura_report.py
from odoo import api, models

class CompraReport(models.AbstractModel):
    _name = 'report.facturas.compra_report_template'
    _description = 'Compra Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['facturas.sales_compras'].browse(docids)
        # Recopilar información de las líneas de factura para cada factura
       
        return {
            'doc_ids': docids,
            'doc_model': 'facturas.sales_compras',
            'docs': docs,
            
        }