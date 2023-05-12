from odoo import models, fields

	class TiquetArchivados(models.Model):
		_inherit = 'helpdesk.ticket'
		filtro_archivados = fields.Boolean(string='Archivados', search='_search_archivados')
		
		def _search_archivados(self, operator, value):
			if value:
				return [('active', '=', False)]
			else:
				return [('active', '=', True)]