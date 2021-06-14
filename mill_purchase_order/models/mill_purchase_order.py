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

class MillPurchaseOrder(models.Model):
    _name = "mill.purchase.order"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = " Mill Purchase Order"
    
    @api.onchange('grade_id') # if these fields are changed, call method
    def _chage_grade_id(self):
        data = []
        for i in self.grade_id.line_ids:
            data.append((0,0,{'element_id':i.element_id,'min_val':i.min_val,'max_val':i.max_val}))
        self.line_ids = data

    @api.onchange('heats') # if these fields are changed, call method
    def _chage_heats(self):
        data = []
        self.material_ordered = 7.50 * self.heats

    @api.depends('basic_rate','extra_rate')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            order.update({
                'net_rate': order.basic_rate + order.extra_rate
            })

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mill.purchase.order') or _('New')
        result = super(MillPurchaseOrder, self).create(vals)
        return result    

    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id                
    
    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner','Supplier')
    date_order = fields.Date(string='Order Date', required=True, index=True, copy=False, default=fields.Date.today)
    date_delivery = fields.Date(string='Delivery Date', required=True, index=True, copy=False, default=fields.Date.today)
    broker_id = fields.Many2one('res.partner','Broker',domain = [('is_broker','=',True)])
    size = fields.Many2one('ingot.size','Material Size')
    finish_size = fields.Many2one('size.size','Finish Size')
    is_ingot = fields.Boolean('Is Ingot',default=True)
    is_finish = fields.Boolean('Is Finish')
    finish_loading = fields.Boolean ("Loading Inclusive")
    cc_size = fields.Char('CC Size')
    grade_id = fields.Many2one('material.grade','Material Grade')
    material_ordered = fields.Float('Material Qty Ordered')
    material_received = fields.Float('Material Qty Received')
    state = fields.Selection([
        ('order_placed', 'Order Placed'),
        ('done', 'Done'),
        ('cancel','Cancelled')
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='order_placed')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',default=_get_default_currency_id)    
    basic_rate = fields.Monetary('Basic Rate',currency_field = "currency_id")
    extra_rate = fields.Monetary('Extra Rate',currency_field = "currency_id")
    net_rate = fields.Monetary(string='Net Rate', store=True, readonly=True,currency_field = "currency_id", compute='_amount_all', track_visibility='always')
    line_ids = fields.One2many('composition.line','purchase_order_id','Composition Line')
    material_feature_ids = fields.Many2many('material.feature','mill_purchase_order_material_feature_rel','order_id','feature_id','Features')
    heats= fields.Float('Heats')