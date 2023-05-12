# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Sale Order Disable Followers | Restricts Customers Add As Followers In Quotation | Restricts Customers Add As Followers In Sale Order",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "license": "OPL-1",
    "summary": "Hide Followers,Auto Add Followers,Invisible Followers,Partner Not Add In Follower, Customer Not Add In Follower, Vendor Not Add In Followers,restrict customer as followers,restrict followers,Disable Followers Odoo",
    "description": """ Generally in the odoo automatically customers are added as followers in sale order/quotation. so our module restricts that. This module disables the customers automatically added as followers in sale order/quotation. This module includes,

1) Confirmation Quotation: When you confirm the quotation the customers are not added as the followers.
2) Send By Email: When you press send by email button in the sale order/quotation the customers are not added as followers.
3) Salesperson As Followers: When you confirm the quotation it restricts the salesperson automatically added as followers.""",
    "version": "14.0.1",
    "depends": [
                "sale_management",
                
    ],
    "application": True,
    "data": [
        'views/res_config_setting.xml',

    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 10,
    "currency": "EUR"
}
