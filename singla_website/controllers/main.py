# -*- coding: utf-8 -*-
from odoo import http

class SinglaWebsite(http.Controller):
    
#     @http.route('/page/aboutus/', type='http', auth="public", website=True)
#     def index(self, **kw):
#         return http.request.render('singla_website.singla_website_aboutus', {'title':' | '.join(['About Us','SSAI'])})
    
    @http.route('/page/products/', type='http', auth="public", website=True)
    def index(self, **kw):
        return http.request.render('singla_website.singla_website_products', {'title':' | '.join(['Products','SSAI'])})    

