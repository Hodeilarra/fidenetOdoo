{
    'name': 'Cointel RMA Reparaciones',
    'summary': """Add an option to create repairs from RMA and manage repairs to create a delivery note""",
    'author': "Shunkawakan",
    'support': 'contact@probuse.com',
    'version': '1.2.2',
    'category': 'Services/Stock',
    'depends': [
                'rma',
                'base',
                'stock',
                'repair'
                ],
    'data':[
        'views/cointel_rma.xml',
        'views/rma_reparacion.xml',
        'views/cointel_reparaciones.xml'
    ],
    'installable' : True,
    'application' : False,
}
