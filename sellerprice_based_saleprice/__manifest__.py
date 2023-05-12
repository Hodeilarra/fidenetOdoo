# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Seller price and standard_price based on list price.",
    "summary": "This module adds a rate of discount, in res partner, to be applied to list_price to obtain "
               "standard_price and seller price in seller ids. Calculation will be launched onchange of: "
               "seller_discount, list_price, seller_id",
    "version": "14.0.1.0.0",
    "author": "Zigor Lekaroz",
    "website": "",
    "license": "AGPL-3",
    "category": "Extra Tools",
    "depends": ["base", "purchase"],
    "data": [
        "views/res_partner.xml",
    ],
    "installable": True,
}
