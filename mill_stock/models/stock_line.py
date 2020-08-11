from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class StockRoll(models.Model):
    _name = "stock.roll"
    _description = "Stock Rolled and Rcvd"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('stock.roll') or _('New')
        result = super(StockRoll, self).create(vals)
        return result
    
    name = fields.Char('Name',default = '/',required = True)
    date = fields.Char('Date',required=True,default = fields.Date.today)
    remarks = fields.Text('Remarks')
    line_id = fields.Many2one('stock.line','Stock Line')
    qty = fields.Float('Qty')    


class StockLine(models.Model):
    _name = 'stock.line'
    _description = "Stock Line"
    _order = "date desc"
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('stock.line') or _('New')
        result = super(StockLine, self).create(vals)
        return result
    
    @api.one
    @api.depends()
    def _compute_stock_balance(self):
        total = 0.00
        for i in self.stock_roll_ids:
            total = total + i.qty
        self.trade_balance = max(self.qty - total,0)
        
    @api.one
    @api.depends()
    def _compute_heat_no(self):
        sizes_list = map(lambda x:x.name + "(" + x.state +  ")"  ,self.heat_ids)
        self.heat_no = ' | '.join(sizes_list)
         
    @api.depends()    
    @api.one
    def _compute_roll_sizes(self):
        for i in self.heat_ids:
            self.roll_size += i.roll_size
            
    name = fields.Char('Name',default = '/',required = True)
    date = fields.Char('Date',required=True,default = fields.Date.today)
    remarks = fields.Text('Remarks')
    partner_id = fields.Many2one('res.partner',help="Mostly furnce, but depends on usage",string = "Partner")
    grade_id = fields.Many2one('material.grade',string = "Material Grade",required=True)
    type = fields.Selection(selection = [('production','Production'),('purchase','Purchase'),('adjustment','Adjustment Entry'),('trade','Trading')],
                            string = "Type",help = "Determines the purpose for which the line has been created",required=True)
    qty = fields.Float('Qty')
    purchase_id = fields.Many2one('mill.purchase.order','Purchase Order')
    pcs = fields.Float('Pcs')
    heat_no = fields.Char('Heat No.(Deprecated)',help = "This field has been deprecated.",compute = "_compute_heat_no")
    heat_no_ids = fields.Many2many('heat.heat','stock_line_heat_heat_relation','stock_line_id','heat_id','Heats')
    state = fields.Selection(selection=[('stock','Stock Updated'),('heats','Heats Updated'),('no_check','Checking Not Required')],default = "stock",required=True)
    trade_state = fields.Selection(selection = [('ingot','Ingot'),('rolled','Rolled'),('dispatch','Dispatch'),('rejected','Rejected')],default = "ingot")
    heat_ids = fields.One2many('heat.heat','stock_line_id','Heats')
    truck_no = fields.Char('Truck No.')
    rolling_id = fields.Many2one('res.partner',"Rolling At")
    roll_size = fields.Many2many('size.size',string = "Rolling Size",compute = "_compute_roll_sizes",help = "In case of trading, the size to be rolled")
    stock_roll_ids = fields.One2many('stock.roll','line_id','Material Rolled')
    trade_balance = fields.Float('Balance',compute = "_compute_stock_balance")
    
    
    