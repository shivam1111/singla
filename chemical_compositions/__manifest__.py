# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Chemical Compositions',
    'version': '1.0',
    'category': 'singla',
    'sequence': 15,
    'summary': 'Chemical Compositions',
    'description': """

    """,
    'website': 'https://www.odoo.com',
    'depends': ['base','mail','mill_order'],
    'data': [
        'views/chemical_composition_view.xml',
        'data/ir_sequence_data.xml',
        'report/chemical_composition_report.xml',
        'report/material_grade_report.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'css': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
