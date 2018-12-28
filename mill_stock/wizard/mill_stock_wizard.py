from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _


class MillStockWizard(models.TransientModel):
    _name = "mill.stock.wizard"
    _description = "Mill Stock Analysis"
    
    @api.one
    @api.depends('date')
    def _compute_total_stock(self):
        total = 0.00
        stock_line_ids = self.env['stock.line'].search([('date','<=',self.date)])
        for i in stock_line_ids:
            total += i.qty
        self.total_stock = total    
    
    @api.one
    @api.depends('from_date','to_date','type')
    def _compute_stock_lines(self):
        domain = [('date','>=',self.from_date),('date','<=',self.to_date)]
        if self.type != 'all':
            domain.append(('type','=',self.type))
        stock_line_ids = self.env['stock.line'].search(domain)
        self.stock_line_ids = stock_line_ids
        total = 0.00
        for i in stock_line_ids:
            total += i.qty 
        self.total_stock_entries = total       
        
    @api.multi
    def print_stock_entries(self):
        return self.env['report'].get_action(self, 'mill_stock.template_mill_stock_wizard_report')
    
    from_date = fields.Date('From',required=True)
    to_date = fields.Date('To',required=True)
    date = fields.Date('Stock on Date')
    type = fields.Selection(selection = [('production','Production'),
                                         ('purchase','Purchase'),('adjustment','Adjustment Entry'),('all','All')],
                            string = "Type",help = "Determines the purpose for which the line has been created",required=True)
    total_stock = fields.Float(string = "Total Stock" ,compute = "_compute_total_stock")
    stock_line_ids = fields.Many2many('stock.line','mill_stock_wizard_stock_line','wizard_id','line_id',
                                      compute = "_compute_stock_lines",
                                      string = 'Stock Lines')
    
    total_stock_entries = fields.Float(string = "Total Stock" ,compute = "_compute_stock_lines")