# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "prueba",
    "summary": "Adds the sale line position to the delivery report lines",
    "version": "14.0.1.0.0",
    "category": "Delivery",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/stock-logistics-reporting",
    "depends": ["res.partner"],
    "data": [
        "views/prueba.xml",
        "security/ir.model.access.csv"
    ],
    "installable": True,
}