# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SSAI Website',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Website Module',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','website_crm'],
    'data': [
        'views/website_templates.xml',
        'views/homepage.xml',
        'views/footer.xml'
    ],
    'demo': [
    ],
    'css': ['static/src/css/*.css'],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}