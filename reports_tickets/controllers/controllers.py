# -*- coding: utf-8 -*-
# from odoo import http


# class ReportsTickets(http.Controller):
#     @http.route('/reports_tickets/reports_tickets/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reports_tickets/reports_tickets/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reports_tickets.listing', {
#             'root': '/reports_tickets/reports_tickets',
#             'objects': http.request.env['reports_tickets.reports_tickets'].search([]),
#         })

#     @http.route('/reports_tickets/reports_tickets/objects/<model("reports_tickets.reports_tickets"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reports_tickets.object', {
#             'object': obj
#         })
