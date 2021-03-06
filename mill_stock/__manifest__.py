# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mill Stock',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Stock Management',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','mill_order','chemical_compositions','mill_purchase_order'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/material_grade_view.xml',
        'views/mill_purchase_order_view.xml',
        'wizard/mill_stock_wizard_view.xml',
        'wizard/mill_stock_wizard_report.xml',
        'security/ir.model.access.csv',
        'report/heat_report.xml',
        'views/heat_view.xml',
        'views/mill_stock_view.xml',
        'views/chemical_composition_view.xml',
        'views/test_test_view.xml',
        'report/test_report.xml',
        'report/test_report_print.xml',
        'views/res_partner_view.xml',
        'report/brokerage_report.xml'
    ],
    'demo': [
    ],
    'css': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
