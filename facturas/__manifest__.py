# -*- coding: utf-8 -*-
{
    'name': "Agencia",

    'summary': """
        Gestión de flujo de presupuestos, albaranes y facturas en un flujo cerrado.
    """,

    'description': """
        Este es una aplicación que trata de crear un nuevo 
        espacio en Odoo para gestionar presupuestos, albaranes y facturas en un flujo cerrado
    """,

    'author': "Aritz Ibañez & Hodei Larrañaga",
    'website': "https://fidenet.net/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail', 'account'],
    

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/invoices.xml',
        'views/templates.xml',
        'views/menus.xml',
        'views/sales_ventas.xml',
        'views/sales_compras.xml',
        'views/albaranes.xml',
        'views/res_partner_view.xml',
        'data/sequence_data.xml',
        'data/sequence_presupuestos.xml',
        'data/sequence_albaran.xml',
        'reports/factura_report_template.xml',
        'reports/venta_report_template.xml',
        'reports/compra_report_template.xml',
        'reports/albaran_report_template.xml',
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    #Indicamos que es una aplicación
    'application': True,
}
