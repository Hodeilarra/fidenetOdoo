# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math
import re

def ean_checksum(eancode):
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode) == int(eancode[-1])


def generate_ean(ean):
    if not ean:
        return "0000000000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:13]
    if len(ean) < 13:
        ean = ean + '0' * (13 - len(ean))
    return ean[:-1] + str(ean_checksum(ean))

class RepairOrder(models.Model):
	_inherit = 'repair.order'

	@api.model
	def create(self, vals_list):
		templates = super(RepairOrder, self).create(vals_list)
		ean = generate_ean(str(templates.id))
		templates.barcode = ean
		return templates

	#date = fields.Datetime('Fecha Estimada')
	date = fields.Date('Fecha Estimada')
	estimate_date = fields.Datetime('Fecha Estimada')
	hours = fields.Float('Horas Dedicadas')
	user_id = fields.Many2one('res.users', string="Responsable", default=8)
	barcode = fields.Char('Código de Barras')

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	man_reference = fields.Char('Referencia de Fabricación')
	sup_reference = fields.Char('Referencia de Proveedor')
