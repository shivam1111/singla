# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2017 darkknightapps@gmail.com
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from odoo import http, tools, _
from odoo.http import request

from odoo.addons.website.controllers.main import Home as WebsiteHome

class Website(WebsiteHome):
    
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        company = request.env.user.company_id
        page_views = company.website_page_visit_count or 0
        page_views += 1
        request.session.update({'page_visit_counter': page_views})
        return super(Website, self).index(**kw)