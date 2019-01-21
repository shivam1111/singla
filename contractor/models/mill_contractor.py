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
from odoo.modules.module import get_module_resource

class AdvanceLine(models.Model):
    _name = "advance.line"
    _description  = "Advance Line"
    _order = "date desc"
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('advance.line') or _('New')
        result = super(AdvanceLine, self).create(vals)
        return result                   
    
    name = fields.Char('Name',default = "/")   
    date = fields.Date('Date',default = fields.Date.today)
    type = fields.Selection([('give','Give Advance'),('return','Return Advance')],required = True)
    amount = fields.Float('Amount') 
    remarks = fields.Text('Remarks')
    contractor_id = fields.Many2one('mill.contractor','Contractor')
    
class ContractorPaymentLine(models.Model):
    _name = "contractor.payment.line"
    _description = "Contractor Payment Line"
    _order = "date desc"
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('contractor.payment.line') or _('New')
        result = super(ContractorPaymentLine, self).create(vals)
        return result                   
    
    name = fields.Char('Name',default = "/")
    date = fields.Date('Date',default = fields.Date.today)
    payment = fields.Float('Payment')
    remarks = fields.Text('Remarks')
    contractor_id = fields.Many2one('mill.contractor','Contractor')

class ContractorMTLine(models.Model):
    _name = "contractor.mt.line"
    _description = "Contractor MT Line"
    _order = "date desc"
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('contractor.mt.line') or _('New')
        result = super(ContractorMTLine, self).create(vals)
        return result                   
    
    @api.onchange('qty','rate')
    def _compute_qty(self):
        self.to_pay  = (self.qty * self.rate)
    
    name = fields.Char('Name',default = "/")
    date = fields.Date('Date',default = fields.Date.today)
    qty = fields.Float('Qty')
    rate = fields.Float('Rate' )
    partner_id = fields.Many2one('res.partner','Partner')
    to_pay = fields.Float('To Pay')
    remarks = fields.Text('Remarks')
    contractor_id = fields.Many2one('mill.contractor','Contractor')
    

class MillContractor(models.Model):
    _name = "mill.contractor"
    _description = "Mill Contractor"
    
    @api.model
    @api.depends('mt_line_ids','mt_line_ids.qty','mt_line_ids.rate','mt_line_ids.to_pay')
    def _compute_total_cost(self):
        self._cr.execute('SELECT SUM(to_pay) from contractor_mt_line')
        total = self._cr.fetchone()[0] or 0.00
        self.total_cost = total

    @api.model
    @api.depends()
    def _compute_total_paid(self):
        total_paid  = 0.00
        for i in self.payment_line_ids:
            total_paid += i.payment
        advance = 0.00
        for i in self.advance_ids.filtered(lambda l: l.type == 'return'):
            advance += i.amount
        self.total_payment = (total_paid + advance)        

    @api.model
    @api.depends('total_cost','total_payment')
    def _compute_balance(self):
        self.balance = self.total_cost - self.total_payment                

    @api.model
    @api.depends()
    def _compute_cost_per_mt(self):
        self._cr.execute('SELECT SUM(qty) from contractor_mt_line')
        total_qty = self._cr.fetchone()[0] or 0.00
        try:
            cost_per_mt = self.total_cost/float(total_qty)
        except ZeroDivisionError:
            cost_per_mt = 0.00
            
        self.cost_per_mt = cost_per_mt
        self.total_qty = total_qty
    
    @api.model
    @api.depends()
    def _compute_advance(self):
        advance = 0.00
        for i in self.advance_ids:
            if i.type == 'give':
                advance += i.amount
            else:
                advance -= i.amount
        self.advance = advance
        
    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))    
    
    name = fields.Char('Name')
    image = fields.Binary("Photo", default=_default_image, attachment=True,
        help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
        help="Medium-sized photo of the employee. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")    
    mt_line_ids = fields.One2many('contractor.mt.line','contractor_id','MT Lines')
    payment_line_ids = fields.One2many('contractor.payment.line','contractor_id','Payment Lines')
    total_cost = fields.Float('Totoal Cost',compute = "_compute_total_cost")
    total_payment = fields.Float('Total Paid',compute = "_compute_total_paid")
    balance = fields.Float('Balance',compute = "_compute_balance",help = "-ve means contractor ows us money")
    cost_per_mt = fields.Float('Cost/MT',compute = "_compute_cost_per_mt")
    total_qty = fields.Float('Total Qty',compute = "_compute_cost_per_mt")
    advance_ids = fields.One2many('advance.line','contractor_id','Advance Lines')
    advance = fields.Float('Advance',compute = "_compute_advance")