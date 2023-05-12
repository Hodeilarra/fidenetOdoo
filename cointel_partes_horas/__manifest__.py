# -*- coding: utf-8 -*-
{
    'name': "Cointel partes de horas",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Adds new value to table
    """,

    'author': "Hodei Larrañaga Unzueta",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "14.0.1.0.0",

    # any module necessary for this one to work correctly
    "depends": [
        "helpdesk_mgmt_project",
        "hr_timesheet",
        "project_timesheet_time_control",
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ]
}
