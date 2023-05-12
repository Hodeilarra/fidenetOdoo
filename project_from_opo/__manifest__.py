# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Proyecto de una oportunidad',
    'version': '1.0',
    'category': 'Extra tools',
    'summary': 'De oportunidad a proyecto.',
    'description': """
Este modulo permite que cuando una oportunidad de crm llegue al estado de ganado, automáticamente se cree un proyecto asociado.
    """,
    'depends': ['crm', 'project'],
    'data': [
        
        'views/project_project_views.xml'
        
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
