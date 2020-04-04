# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2017 darkknightapps@gmail.com
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################

from odoo import fields, models

class Company(models.Model):
    _inherit = "res.company"
    
    website_page_visit_count = fields.Integer(string='Website Page Visits',
                                              help='Number of page views for your website.')