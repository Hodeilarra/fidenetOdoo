# -*- coding: utf-8 -*-
{
    'name': "modificacion_reparaciones",

    'summary': """
        Save the sale order""",

    'description': """
        Create a quotation when we create a repair order, modify the repair ticket to add a barcode.
    """,

    'author': "Shunkawakan ZUbizarreta",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "14.0.1.0.0",

    # any module necessary for this one to work correctly
    'depends': ['base', 'repair', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'reports/repair_tutorial_report_inherit.xml',
    ]
}
