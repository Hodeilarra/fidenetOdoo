# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _


class WizStockBarcodesRead(models.AbstractModel):
    _inherit = "wiz.stock.barcodes.read"

    is_qr = fields.Boolean('Is QR Code', default=True)
    allow_duplicated = fields.Boolean('Allow duplicated', default=False)

    def process_barcode(self, barcode):
        ICP = self.env["ir.config_parameter"].sudo()
        if not self.is_qr and not self.product_id:
            if len(barcode) > int(ICP.get_param("custom_stock_barcode.qr_min_length", "16")):
                self._set_messagge_info("info",
                                        _("Length error, are you sure you are reading a NOT QR barcode?"))
                self.play_sounds(False)
                return
            return super(WizStockBarcodesRead, self).process_barcode(barcode)
        if self.is_qr:

            position_barcode = int(ICP.get_param("custom_stock_barcode.position_barcode", "0"))
            position_sn = int(ICP.get_param("custom_stock_barcode.position_serial_number", "1"))
            position_mac = int(ICP.get_param("custom_stock_barcode.position_mac", "9"))
            lot_name_structure = ICP.get_param("custom_stock_barcode.lot_name_structure", "%s-%s")

            decoded, list_length = self.barcode_parse(barcode)
            if not decoded:
                self._set_messagge_info("info", _("Length error, check string separator and length in System parameters"))
                return
            barcode = decoded[position_barcode]
            if list_length > position_mac:
                lot_name = lot_name_structure % (decoded[position_sn], decoded[position_mac])
            else:
                lot_name = decoded[position_sn]
            self._set_messagge_info("success", _("Barcode read correctly"))
            domain = self._barcode_domain(barcode)
            product = self.env["product.product"].search(domain)
        else:
            """Si no es un QR y hay producto no cambiamos el producto, cada lectura será un SN"""
            product = self.product_id
            lot_name = barcode
        if product:
            if len(product) > 1:
                self._set_messagge_info("more_match", _("More than one product found"))
                return
            self.product_id = product
            self.lot_id = self.search_lot(lot_name)
            """Si no hay lot_id y es un albarán de entrada intentamos crear el lot_id"""
            if not self.lot_id and self.picking_id and self.picking_id.picking_type_id.code == 'incoming':
                lot_dict = {"product_id": self.product_id.id,
                            "name": lot_name,
                            "company_id": self.env.company.id}
                self.lot_id = self.env['stock.production.lot'].create(lot_dict)

            self.action_product_scaned_post(product)
            self.action_done()
            self.play_sounds(True)
            return
        if self.env.user.has_group("product.group_stock_packaging"):
            packaging = self.env["product.packaging"].search(domain)
            if packaging:
                if len(packaging) > 1:
                    self._set_messagge_info(
                        "more_match", _("More than one package found")
                    )
                    return
                self.action_packaging_scaned_post(packaging)
                self.action_done()
                return
        if self.env.user.has_group("stock.group_production_lot"):
            lot_domain = [("name", "=", lot_name)]
            if self.product_id:
                lot_domain.append(("product_id", "=", self.product_id.id))
            lot = self.env["stock.production.lot"].search(lot_domain)
            if len(lot) == 1:
                self.product_id = lot.product_id
            if lot:
                self.action_lot_scaned_post(lot)
                self.action_done()
                return
        location = self.env["stock.location"].search(domain)
        if location:
            self.location_id = location
            self._set_messagge_info("info", _("Waiting product"))
            return
        self._set_messagge_info("not_found", _("Barcode not found"))

    def search_lot(self, lot_name):
        if lot_name:
            lot_id = self.env['stock.production.lot'].search([('name', '=', lot_name),
                                                              ('product_id', '=', self.product_id.id)])
            if lot_id:
                return lot_id
            else:
                return False

    def barcode_parse(self, barcode):
        ICP = self.env["ir.config_parameter"].sudo()
        split_char = ICP.get_param("custom_stock_barcode.string_separator", ";")
        decoded = barcode.split(split_char)
        list_length = len(decoded)
        """No ha podido hacer el split. La lista es de un elemento algo raro ha pasado"""
        if list_length == 1:
            return False, False
        else:
            return decoded, list_length

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.is_qr is False:
            self.write({'product_id': self.product_id})

    def check_location_contidion(self):
        if not self.location_id:
            self.location_id = self.picking_id.location_id
        return super().check_location_contidion()
