# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Custom Stock Barcodes",
    "summary": "Read barcode and split it to get product barcode and lot name",
    "version": "14.0.1.5.0",
    "author": "Zigor Lekaroz",
    "website": "",
    "license": "AGPL-3",
    "category": "Extra Tools",
    "depends": ["stock", "stock_barcodes"],
    "data": [
        "data/ir_config_parameter.xml",
        "views/stock_barcodes_new_lot_view.xml",
        "wizard/stock_barcodes_read_picking_views.xml",
    ],
    "installable": True,
}
