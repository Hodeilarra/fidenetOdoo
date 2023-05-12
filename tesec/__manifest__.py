# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Order Create from Project Task',
    'license': 'Other proprietary',
    'summary': """Create Customer Sale/ Order from Project Tasks.""",
    'description': """
Project Task Create a Sale Order 
    """,
    'author': "Shunkawakan ZUbizarreta",
    'images': ['static/description/image.png'],
    'version': '1.2.2',
    'category': 'Services/Project',
    'depends': [
                'project',
                'sale',
                'account'
                ],
    'data':[
        'security/ir.model.access.csv',
        'views/project_task_form_view.xml',
        'views/project_project_view.xml',
        'views/sale_order_nombre_obra_form_view.xml',
        'views/account_move_nombre_obra_form_view.xml'
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
