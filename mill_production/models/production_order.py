from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class ProductionOrderLine(models.Model):
    _name="production.order.line"
    _description = "Production Order Line"
    _order = "sequence"
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('production.bundle') or _('New')
        result = super(ProductionOrderLine, self).create(vals)
        return result               
    
    @api.onchange('pcs','kg_per_pc')
    def _compute_qty(self):
        self.qty  = (self.kg_per_pc * self.pcs)/1000    
    
    name = fields.Char('Name', help = "This is also a bundle No.",default = '/')
    size_id = fields.Many2one('size.size',string  = "Size",required = True)
    tolerance = fields.Char('Tolerance')
    corner_id = fields.Many2one('corner.type',string = "Corner Type",related = "size_id.corner_id",store=True)
    sequence = fields.Integer('sequence', help="Sequence for the handle.",default=10)
    pcs = fields.Float('Pcs')
    kg_per_pc = fields.Float('Kg/pc')
    qty = fields.Float('Qty')
    grade_id = fields.Many2one('material.grade','Grade')
    partner_id = fields.Many2one('res.partner',help="Mostly furnce, but depends on usage",string = "Partner")
    cc = fields.Char('Clear Cut (CC)')
    production_id = fields.Many2one('production.order','Production Order')
    heat_no = fields.Char('Heat No.')
    remarks = fields.Char('Remarks')
    
class ProductionOrder(models.Model):
    _name = "production.order"
    _description = "Production Order"
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('production.order') or _('New')
        result = super(ProductionOrder, self).create(vals)
        return result            
    
    name = fields.Char('Name',default = '/')
    date = fields.Date('Date',required=True,default = fields.Date.today)
    line_ids = fields.One2many('production.order.line','production_id','Order Lines')
    remarks = fields.Text('Remarks')
    