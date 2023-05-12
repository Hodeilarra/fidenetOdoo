{
    'name': 'Create Sales Order From POS',
    'version': '14.0.1.0.3',
    'category': 'Sales/Point of Sale',
    'summary': 'Create sale order from pos screen and view the sales order created fom pos',
    'description': '''
    ''',
    'author': 'Warlock Technologies Pvt Ltd.',
    'website': 'http://warlocktechnologies.com',
    'support': 'support@warlocktechnologies.com',
    'depends': ['point_of_sale', 'sale_management'],
    "data": ['views/pos_config.xml','views/assests.xml'],
    'qweb': [
        'static/src/xml/Screens/ProductScreen/ControlButtons/SaleOrderButton.xml',
        'static/src/xml/Screens/ProductScreen/ControlButtons/ViewSalesOrderButton.xml',
        'static/src/xml/Screens/SaleOrderScreen/SaleOrderScreen.xml',
        'static/src/xml/Screens/SaleOrderScreen/ViewSaleOrderList.xml',
        'static/src/xml/Screens/SaleOrderScreen/ViewSaleOrderRow.xml',
        'static/src/xml/Popups/SalesOrderPopup.xml',
    ],
    'images': ['static/images/screen_image.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
    'external_dependencies': {
    },
}
