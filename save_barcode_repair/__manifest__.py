# -*- coding: utf-8 -*-
{
    'name': "save_barcode_repair",

    'summary': """
        Save the barcode""",

    'description': """
        Save the barcode value in Point of sale module
    """,

    'author': "Shunkawakan ZUbizarreta",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "14.0.1.0.0",

    # any module necessary for this one to work correctly
    'depends': ['base', 'repair'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ]
}
