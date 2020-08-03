from odoo import tools
from odoo import api, fields, models


class MillOrderReport(models.Model):
    _name = "mill.order.report"
    _description = "Order Report"
    _auto = False
    
    name = fields.Char('Name')
    order_qty = fields.Float('Order Qty')
    completed_qty = fields.Float('Completed Qty')
    balance = fields.Float('Balance')
    partner_id = fields.Many2one('res.partner',string = "Customer")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel','Cancel'),
        ('done', 'Done'),
        ], string='Status',default='draft')
    grade_id = fields.Many2one('material.grade','Grade')
    
    def _select(self):
        select_str = """
            select 
                min(l.id) as id,
                size,
                SUM(order_qty) as order_qty,
                SUM(completed_qty) as completed_qty,
                SUM(order_qty) - SUM(completed_qty)  as balance,
                partner_id,
                state
        """ 
        return select_str
    
    def _from(self):
        from_str = """
            mill_order  l
        """
        return from_str
        
    def _group_by(self):
        group_by_str = """
            GROUP BY partner_id,size,state 
                    
        """
        return group_by_str    
    
    @api.model_cr
    def init(self):
        # self._table = mill_order_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s 
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

