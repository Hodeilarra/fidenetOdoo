# Copyright 2009 Akretion,Guewen Baconnier,Camptocamp,Avanzosc,Sharoon Thomas,Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
     'name': 'Pos order report',
    'summary': """Añadimos opción de imprimir los pedidos de venta""",
    'author': "Hodei Larrañaga Unzueta",
    'support': '',
    "license": "AGPL-3",
    'version': '1.0.0',
    'category': 'point_of_sale',
    'depends': [
                'base','point_of_sale'
                ],
   'data': [
        'views/pos_order_report.xml',
        'views/pos_order_report_action.xml',
        'views/report_pos_order_template.xml',
        
    ],
    'installable' : True,
    'application' : False,
}

