# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "pos_custom_buttons",
    "summary": "Adds a button on POS",
    "version": "14.0.1.0.0",
    "category": "Point of Sale",
    "author": "Shunkawakan Zubizarreta",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/stock-logistics-reporting",
    'depends': ['base', 'point_of_sale'],
    'data': [
    'views/templates.xml',
    ],

    'qweb': [
        'static/src/xml/AliasButton.xml',
    ],

    'assets': {
        'point_of_sale.assets': [
            'numenapp_buyer_name/static/src/js/**/*',
        ],
    },
    "installable": True,
}