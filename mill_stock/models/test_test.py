# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2013 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo import tools, _

class TestLine(models.Model):
    _name = "test.line"
    _description = "Test Line"
    
    @api.onchange('heat_id')
    def onchange_heat_id(self):
        if self.heat_id:
            self.heat_print_name = self.heat_id.name_get()[0][1]
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('test.line') or _('New')
        result = super(TestLine, self).create(vals)
        return result        
    
    name = fields.Char('Name',default = '/',required = True)
    supplier_id = fields.Many2one('res.partner','Supplier')
    grade_id = fields.Many2one('material.grade','Grade')
    heat_id = fields.Many2one('heat.heat','Heat No.')
    heat_print_name = fields.Char('Heat Print Name',required=True)
    remarks = fields.Char('Remarks')
    date = fields.Date('Date',default = fields.Date.today,requred=True)
    test_id = fields.Many2one('test.test',string = "Test",ondelete='cascade', index=True, copy=False)

class Test(models.Model):
    _name = "test.test"
    _description = "Test"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('test.test') or _('New')
        result = super(Test, self).create(vals)
        return result    
    
    name = fields.Char('Name',default = '/',required = True)
    partner_id = fields.Many2one('res.partner','Lab',required=True)
    date = fields.Date('Date',default = fields.Date.today)
    line_ids = fields.One2many('test.line','test_id','Test Lines')
    
    