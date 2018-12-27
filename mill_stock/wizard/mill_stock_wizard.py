from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _


class MillStockWizard(models.TransientModel):
    _name = "mill.stock.wizard"
    _description = "Mill Stock Analysis"
    
    @api.one
    @api.depends('date','type')
    def _compute_total_stock(self):
        total = 0.00
        stock_line_ids = self.env['stock.line'].search([('date','<=',self.date)])
        for i in stock_line_ids:
            total += i.qty
        self.total_stock = total    
    
    from_date = fields.Date('From',required=True)
    to_date = fields.Date('To',required=True)
    date = fields.Date('Stock on Date')
    type = fields.Selection(selection = [('production','Production'),
                                         ('purchase','Purchase'),('adjustment','Adjustment Entry'),('all','All')],
                            string = "Type",help = "Determines the purpose for which the line has been created",required=True)
    total_stock = fields.Float(string = "Total Stock" ,compute = "_compute_total_stock")
    
    