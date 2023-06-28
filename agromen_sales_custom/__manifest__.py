# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Personalización de Ventas',
    'category': 'Sales',
    'summary': 'Varias personalizaciones en el modulo de ventas',
    'version': '1.0',
    'depends': ['sale_management', 'account', 'project'],
    'data': [
       

        'views/sale_order_view.xml',
        'views/project_view.xml',
        'views/account_analytic_view.xml',
       
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
