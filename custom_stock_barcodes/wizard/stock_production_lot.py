# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WizStockBarcodesNewLot(models.TransientModel):
    _inherit = "wiz.stock.barcodes.new.lot"

    def on_barcode_scanned(self, barcode):
        ICP = self.env["ir.config_parameter"].sudo()
        position_barcode = int(ICP.get_param("custom_stock_barcode.position_barcode", "0"))
        position_sn = int(ICP.get_param("custom_stock_barcode.position_serial_number", "1"))
        position_mac = int(ICP.get_param("custom_stock_barcode.position_mac", "9"))
        lot_name_structure = ICP.get_param("custom_stock_barcode.lot_name_structure", "%s-%s")

        decoded, list_length = self.barcode_parse(barcode)
        if not list_length:
            raise ValidationError(_("An error occurred. This may be caused by split char misconfiguration."))
        barcode = decoded[position_barcode]
        if list_length > position_mac:
            lot_name = lot_name_structure % (decoded[position_sn], decoded[position_mac])
        else:
            lot_name = decoded[position_sn]
        product = self.env["product.product"].search([("barcode", "=", barcode)])[:1]
        if product and not self.product_id:
            self.product_id = product
        elif not product and not self.product_id:
            raise ValidationError(_("Product with barcode %s not found. "
                                    "Check if there is a product with barcode %s." % (barcode, barcode)))
        self.lot_name = lot_name

    """Este método es copia destock_barcodes_read.py, pq este wizard no hereda del wiz stock_barcode_read
    Lo repito para poder usarlo aquí"""
    def barcode_parse(self, barcode):
        ICP = self.env["ir.config_parameter"].sudo()
        split_char = ICP.get_param("custom_stock_barcode.string_separator", ";")
        decoded = barcode.split(split_char)
        """No ha podido hacer el split. La lista es de un elemento algo raro ha pasado"""
        list_length = len(decoded)
        if list_length == 1:
            return False, False
        else:
            return decoded, list_length
