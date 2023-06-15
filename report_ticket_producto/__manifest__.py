# -*- coding: utf-8 -*-
{
    'name': "Ticket de producto",

    'summary': """
        Añadimos la opción de imprimir el ticket del producto en papel reducido""",

    'description': """
        Añadimos la opción de imprimir el ticket del producto en papel reducido""",

    'author': "Hodei Larrañaga Unzueta",
    'website': "https://www.fidenet.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'repair'],

    # always loaded
    'data': [
        
        'views/product.xml',
    ],
   
}
