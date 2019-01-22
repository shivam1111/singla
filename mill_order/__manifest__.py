# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mill Order',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Orders Management',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','india_gst'],
    'data': [
        'views/mill_order_view.xml',
        'report/mill_order_report_view.xml',
        'report/packing_list_report.xml',
        'data/ir_sequence_data.xml',
    ],
    'demo': [
    ],
    'css': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
