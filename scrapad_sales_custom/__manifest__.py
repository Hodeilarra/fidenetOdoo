# Copyright 2009 Akretion,Guewen Baconnier,Camptocamp,Avanzosc,Sharoon Thomas,Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
     'name': 'Scrapad personalización ventas y facturación',
    'summary': """Añade campos a presupuestos y facturación y personaliza los informes de presupuestos, """,
    'author': "Hodei Larrañaga Unzueta",
    'support': '',
    "license": "AGPL-3",
    'version': '14.0.1.0.0',
    'website': 'https://www.fidenet.net',
    'category': 'sale',
    'depends': [
                'sale','account'
                ],
   'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/report_saleorder_document.xml',
        'views/report_invoice_document.xml',
        
        
    ],
    'images': ['static/description/icon.png'],
    'installable' : True,
    'application' : False,
}

