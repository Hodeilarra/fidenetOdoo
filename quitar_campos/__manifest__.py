{
    'name': 'Quitar campos de factura',
    'version': '1.0',
    'summary': 'Módulo para modificar el reporte de factura',
    'author': 'Hodei Larrañaga Unzueta',
    'website': 'http://www.tu-website.com',
    'category': 'Facturación',
    'description': """
    Este módulo personalizado elimina los campos invoice_date e invoice_payment_term_id del reporte de factura.
    """,
    'depends': ['account','sale'],  # Dependiendo de tu instancia de Odoo, es posible que necesites agregar más dependencias aquí
    'data': [
        'views/report_invoice.xml',
        'views/form_sale.xml',  # Aquí es donde debes colocar el camino hacia el archivo XML que modificas
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}