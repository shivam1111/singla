# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2017 darkknightapps@gmail.com
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from odoo import api, fields, models, _
from odoo.http import request

class Website(models.Model):
    _inherit = "website"
    
    # Editted by Shivam Goyal
    @api.multi
    def get_count_customers(self):
        count = self.env['res.partner'].sudo().search_count([('is_company','=',True),('customer','=',True)])
        return count
    
    @api.multi
    def get_page_view_count(self):
        page_view_count = request.session.get('page_visit_counter', 0)
        self.env.user.company_id.sudo().write({'website_page_visit_count': page_view_count})
        return page_view_count