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
    'depends': ['base','website_crm','website_page_view_count'],
    'data': [
        'views/website_templates.xml',
        'views/homepage.xml',
        'views/footer.xml',
        'views/aboutus.xml',
        'views/products.xml',
        'views/grades.xml',
    ],
    'demo': [
    ],
    'css': ['static/src/css/*.css'],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
