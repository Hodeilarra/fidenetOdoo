# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "point_of_sale_modify",
    "summary": "This module adds a option to load products with a bar code",
    "version": "14.0.1.0.0",
    "author": "Shunkawakan Zubizarreta",
    "website": "",
    "license": "AGPL-3",
    "category": "Extra Tools",
    'depends': ['point_of_sale'],
    'data': ['views/pos_coupon.xml'],
    "qweb":  ['point_of_sale_modify/static/src/xml/point_of_sale_view.xml'],
    "installable": True,
}
