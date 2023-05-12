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
    'data': ['views/pos_templates.xml'],
    "qweb":  ['pos_custom_buttons/static/src/xml/pos_product_button_view.xml'],
    'assets': {
    'point_of_sale.assets': [
        'pos_custom_buttons/static/src/js/**/*',
        ],
    },
    "installable": True,
}