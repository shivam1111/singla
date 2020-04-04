# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2017 darkknightapps@gmail.com
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
{
    'name': "Website Page View Counter",
    'summary': """
        This module is for displaying page visit count in your website. """,
    'description': """ 
        * Page Visit Counter
""",

    'author': 'Dark Knight',
    'website': '',
    'category': 'Website',
    'version': '1.0',
    'depends': ['website'],
    'data': [
        'views/company_view.xml',
    ],
    'demo': [
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
}