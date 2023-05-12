{
    'name': 'Cancel State',
    'summary': """Adds cancel state to inventory and invoice""",
    'author': "Shunkawakan",
    'support': 'contact@probuse.com',
    'version': '1.2.2',
    'category': 'Services/Stock',
    'depends': [
                'stock',
                'account'
                ],
    'data':[
        'views/cointel_cancel_account.xml',
    ],
    'installable' : True,
    'application' : False,
}
