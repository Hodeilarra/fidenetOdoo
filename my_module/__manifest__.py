# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "my_module",
    "summary": "Adds a button on POS",
    "version": "14.0.1.0.0",
    "category": "Point of Sale",
    "author": "Shunkawakan Zubizarreta",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/stock-logistics-reporting",
    'depends': ['base', 'point_of_sale'],
    'data': ['views/template.xml'],
    "qweb":  ['my_module/static/src/xml/customer.xml'],
    'assets': {
    'point_of_sale.assets': [
        'my_module/static/src/js/customer.js',
        ],
    },
    "installable": True,
}