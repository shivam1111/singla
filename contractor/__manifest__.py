# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mill Contractor',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Mill Contractor Management',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','mill_order'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/mill_contractor_view.xml',
        'report/mill_contractor_report_view.xml',
        
    ],
    'demo': [
    ],
    'css': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
