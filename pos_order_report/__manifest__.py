{
    'name': 'Pos order report',
    'summary': """Añadimos opción de imprimir los pedidos de venta""",
    'author': "Hodei Larrañaga Unzueta",
    'support': '',
    "license": "AGPL-3",
    'version': '1.0.0',
    'category': 'point_of_sale',
    'depends': [
                'point_of_sale'
                ],
    'data':[
        'views/pos_order_view.xml',
        'reports/report_pos_order_simplified.xml',
    ],
    'installable' : True,
    'application' : False,
}
