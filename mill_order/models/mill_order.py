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

class CornerType(models.Model):
    _name = "corner.type"
    _description = "Corner Type"
    
    name = fields.Char('Name')

class IngotSize(models.Model):
    _name = "ingot.size"
    _description = "Ingot Size"
    
    name = fields.Char('Name')    
    
class MillOrder(models.Model):
    _name = 'mill.order'
    _description = "Mill Order"
    _rec_name = "size"

    @api.onchange('qty')
    def onchange_qty(self):
        # Considering 69MT production in 11 hours. 6.27/hour
        self.duration = self.qty/6.27
    
    @api.one
    def unlink(self):
        records_to_unlink = self.env['mill.order']
        for o in self:
            records_to_unlink |= self.browse(int(self.id))
        return super(MillOrder,records_to_unlink).unlink()
        
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
    qty = fields.Float('Quantity')
    grade_id = fields.Many2one('material.grade','Grade')
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
    corner_id = fields.Many2many('corner.type',string = "Corner Type")
    booking_date = fields.Date('Booking Date',default = fields.Date.today())
    ingot_size  = fields.Many2one('ingot.size','Ingot Size')
    cut_length = fields.Char('Cut Length')
    completed = fields.Float('Completed')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('manufactured','Manufactured'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')    
    
    
    
