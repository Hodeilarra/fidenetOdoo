# -*- coding: utf-8 -*-
# from odoo import http


# class Cyclos(http.Controller):
#     @http.route('/cyclos/cyclos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cyclos/cyclos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cyclos.listing', {
#             'root': '/cyclos/cyclos',
#             'objects': http.request.env['cyclos.cyclos'].search([]),
#         })

#     @http.route('/cyclos/cyclos/objects/<model("cyclos.cyclos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cyclos.object', {
#             'object': obj
#         })
