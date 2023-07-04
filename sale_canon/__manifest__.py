# Copyright 2022 Obertix - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Canon",
    "version": "13.0.1.0.1",
    "category": "Custom",
    "website": "https://obertix.net",
    "author": "Obertix",
    "license": "AGPL-3",
    "installable": True,
    "summary": "Module to manage spanish canon.",
    "depends": [
        "sale", "website_sale"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/product_canon.xml",
        "data/canon_data.xml",
        "views/product_template_views.xml",
        "views/res_partner_views.xml",
    ],
}
