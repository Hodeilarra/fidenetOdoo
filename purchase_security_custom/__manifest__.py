# Copyright 2022 Obertix - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase security custom",
    "version": "13.0.1.0.1",
    "category": "Purchase",
    "website": "https://fidenet.net",
    "author": "Hodei Larrañaga Unzueta",
    "license": "AGPL-3",
    "installable": True,
    "summary": "Modificamos el campo representante de compra para los usuarios que pertenezcan al grupo group_purchase_own_orders",
    "depends": [
        "base", "purchase", "purchase_security"
    ],
    "data": [
        "views/purchase_order_form_view.xml",
        
    ],
     'images': ['static/description/icon.png'],
    
}
