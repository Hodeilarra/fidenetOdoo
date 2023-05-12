from odoo import models, fields

	#class RMACancelados(models.Model):
	#	_inherit = 'rma'
	#	filtro_cancelados = fields.Boolean(string='Archivados', search='_search_cancelados')
	#	
	#	def _search_cancelados(self, operator, value):
	#		if value:
	#			return [('state', '!=', 'cancel')]
	#		else:
	#			return [('state', '==', 'cancel')]