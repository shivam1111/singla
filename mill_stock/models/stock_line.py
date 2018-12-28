from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _


class StockLine(models.Model):
    _name = 'stock.line'
    _description = "Stock Line"
    _order = "date desc"
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('stock.line') or _('New')
        result = super(StockLine, self).create(vals)
        return result
        
    
    name = fields.Char('Name',default = '/',required = True)
    date = fields.Char('Date',required=True,default = fields.Date.today)
    remarks = fields.Text('Remarks')
    partner_id = fields.Many2one('res.partner',help="Mostly furnce, but depends on usage",string = "Partner")
    grade_id = fields.Many2one('material.grade',string = "Material Grade",required=True)
    type = fields.Selection(selection = [('production','Production'),('purchase','Purchase'),('adjustment','Adjustment Entry')],
                            string = "Type",help = "Determines the purpose for which the line has been created",required=True)
    qty = fields.Float('Qty')
    purchase_id = fields.Many2one('mill.purchase.order','Purchase Order')
    pcs = fields.Float('Pcs')
    heat_no = fields.Char('Heat No.')
    
    