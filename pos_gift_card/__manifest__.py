# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Gift Card",
  "summary"              :  "POS Gift Cards module allows to sell gift cards on Point Of Sale. It also allows to sell multiple variants of the gift cards (based on price). Secret codes are created on sale of Gift Cards and those secret codes are provided to the customers",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Gift-Card.html",
  "description"          :  """https://webkul.com/blog, POS Gift Cards, POS Coupons Cards, POS Card Vouchers, POS Birthday Gift Cards""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_gift_card&version=13.0&custom_url=/pos/auto",
  "depends"              :  [
                             'pos_coupons',
                            ],
  "data"                 :  [
                             'data/gift_card_categ_data.xml',
                             'views/inherited_product_view.xml',
                             'views/pos_order_view.xml',
                            ],
  "demo"                 :  ['data/data.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  50,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
