# -*- coding: utf-8 -*-
from odoo import http

class SinglaWebsite(http.Controller):
    
#     @http.route('/page/aboutus/', type='http', auth="public", website=True)
#     def index(self, **kw):
#         return http.request.render('singla_website.singla_website_aboutus', {'title':' | '.join(['About Us','SSAI'])})
    
    @http.route('/grade/<grade>',type='http', auth="public", website=True)
    def get_grade_detail(self,grade,**kwargs):
        if grade == "spring_steel":
            return http.request.render('singla_website.grade_spring_steel', {'title':' | '.join(['Spring Steel','SSAI'])})
        if grade == "boron_steel":
            return http.request.render('singla_website.grade_boron_steel', {'title':' | '.join(['Boron Steel','SSAI'])})
        return http.request.render('website.404')
    
    @http.route('/page/products/', type='http', auth="public", website=True)
    def index(self, **kw):
        return http.request.render('singla_website.singla_website_products', {'title':' | '.join(['Products','SSAI'])})    

