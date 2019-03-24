# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mill Production',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Production Management',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','chemical_compositions','mill_stock'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/mill_production_view.xml',
        'report/mill_production_report.xml',
        'views/production_order_view.xml',
        'report/production_order_report.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'css': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
