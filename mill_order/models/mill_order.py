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
from odoo.tools.translate import _

class Size(models.Model):
    _name = "size.size"
    _description = "Flats Size"
    
    @api.multi
    def name_get(self):
        result = []
        for i in self:
            result.append((i.id,i.name+" ("+i.corner_id.name+")"))
        return result
    
    name = fields.Char('Size',required=True)
    corner_id = fields.Many2one('corner.type',string = "Corner Type",required=True)
    remarks = fields.Text('Remarks')

class CornerType(models.Model):
    _name = "corner.type"
    _description = "Corner Type"
    
    name = fields.Char('Name')

class IngotSize(models.Model):
    _name = "ingot.size"
    _description = "Ingot Size"
    
    name = fields.Char('Name')    

class MillOrderSizeLine(models.Model):
    _name = "mill.order.size.line"
    _description = "Mill Order Size Line"
    
    @api.one
    @api.depends('order_id.line_completed_ids','order_id.line_completed_ids.completed_qty')
    def _compute_completed_qty(self):
        line_ids = self.order_id.line_completed_ids.filtered(lambda rec: rec.name.id == self.id)
        total = 0.00
        for i in line_ids:
            total = total + i.completed_qty
        self.completed_qty = total
        
    name = fields.Many2one('size.size',required=True)
    order_qty = fields.Float('Order Qty')
    completed_qty = fields.Float('Completed Qty', compute = "_compute_completed_qty",store=True)
    rate = fields.Float("Rate")
    remarks = fields.Text("Remarks")
    corner_id = fields.Many2one('corner.type',string = "Corner Type",related = "name.corner_id",store=True)
    order_id = fields.Many2one('mill.order')
    partner_id = fields.Many2one('res.partner',related = "order_id.partner_id",string = "Customer",store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('manufactured','Manufactured'),
        ('cancel','Cancel'),
        ('done', 'Done'),
        ], string='Status', copy=False, index=True, track_visibility='onchange', default='draft')
    grade_id = fields.Many2one('material.grade','Grade')
    booking_date = fields.Date('Booking Date',default = fields.Date.today)
    cut_length = fields.Char('Cut Length')
    ingot_size  = fields.Many2one('ingot.size','Ingot Size')

class MillOrderSizeLineCompleted(models.Model):
    _name = "mill.order.size.line.completed"
    _description = "Mill Order Size Line Completed"
    
    name = fields.Many2one('mill.order.size.line')
    order_qty = fields.Float('Order Qty',related = "name.order_qty")
    grade_id = fields.Many2one('material.grade','Grade',related = "name.grade_id")
    cut_length = fields.Char('Cut Length',related = "name.cut_length")
    corner_id = fields.Many2one('corner.type',string = "Corner Type",related = "name.corner_id",store=True)
    completed_qty = fields.Float('Completed Qty')
    remarks = fields.Text("Remarks")
    order_id = fields.Many2one('mill.order')
    complete_date = fields.Date('Completion Date')
    pcs = fields.Float('Pcs')
    
class MillOrder(models.Model):
    _name = 'mill.order'
    _description = "Mill Order"
    _rec_name = "size"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    @api.onchange('line_ids')
    def onchange_line_ids(self):
        sizes_list = map(lambda x:x.name and x.name.name or '',self.line_ids)
        self.size = ' | '.join(sizes_list)
    
    @api.onchange('qty')
    def onchange_qty(self):
        # Considering 69MT production in 11 hours. 6.27/hour
        self.duration = self.qty/6.27
    
    @api.one
    def set_state_done(self):
        self.state = 'done'
    
    @api.one
    def write(self,vals):
        if vals.get('state',False) == 'done':
            for l in self.line_ids:
                if l.state != 'cancel':
                    l.state = 'done'
        if vals.get('state',False) == 'cancel':
            for l in self.line_ids:
                l.state = 'cancel'
            
        return super(MillOrder,self).write(vals)
    
    @api.one
    def unlink(self):
        records_to_unlink = self.env['mill.order']
        for o in self:
            records_to_unlink |= self.browse(int(self.id))
        return super(MillOrder,records_to_unlink).unlink()
      
    @api.depends('line_ids','line_ids.order_qty')
    def _compute_qty(self):
        '''
            Compute the total ordered and completed qty
        '''
        for order in self:
            order_qty = sum(map(lambda x:x.order_qty,order.line_ids))
            complete_qty = sum(map(lambda x:x.completed_qty,order.line_ids))
            order.order_qty = order_qty
            order.completed_qty = complete_qty
    
    @api.depends('rate','extra_rate','rolling')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            order.update({
                'net_rate': order.rate + order.extra_rate + order.rolling
            })
        
    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id                
            
    size = fields.Char(string='Size', required=True)
    order_qty = fields.Float('Quantity',compute = '_compute_qty')
    qty = fields.Float('Old field Qty')
    partner_id = fields.Many2one('res.partner','Customer',required=True)
    manufacturing_date = fields.Datetime('Manufacturing Date')
    duration = fields.Float('Duration')
    note = fields.Text('Note')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',default=_get_default_currency_id)        
    rate = fields.Monetary('Basic Rate/MT',currency_field = "currency_id")
    extra_rate = fields.Monetary('Extra Rate',currency_field = "currency_id")
    rolling = fields.Monetary('Rolling',currency_field = "currency_id")
    net_rate = fields.Monetary(string='Net Rate', store=True, readonly=True,currency_field = "currency_id", compute='_amount_all', track_visibility='always')
    booking_date = fields.Date('Booking Date',default = fields.Date.today)
    completed = fields.Float('Old field Completed Qty')
    completed_qty = fields.Float('Completed',compute = '_compute_qty')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel','Cancel'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    line_ids = fields.One2many('mill.order.size.line','order_id','Order Lines')    
    line_completed_ids = fields.One2many('mill.order.size.line.completed','order_id','Completed Order Lines')
    
    
