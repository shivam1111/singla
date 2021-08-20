# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mill Purchase Order',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Mill Purchase Orders Management',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','mill_order','chemical_compositions'],
    'data': [
        'views/mill_purchase_order_view.xml',
        'views/res_partner_view.xml',
        'data/ir_sequence_data.xml',
        'report/purchase_order_summary_report.xml',
    ],
    'demo': [
    ],
    'css': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
