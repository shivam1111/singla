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
                min(o.id) as id,
                s.name as name,
                SUM(l.order_qty) as order_qty,
                o.completed_qty as completed_qty,
                SUM(o.order_qty - o.completed_qty)  as balance,
                l.grade_id as grade_id,
                o.partner_id,
                o.state
        """ 
        return select_str
    
    def _from(self):
        from_str = """
            mill_order  o right join mill_order_size_line l on o.id = l.order_id right join size_size s on s.id = l.name
        """
        return from_str
        
    def _group_by(self):
        group_by_str = """
            GROUP BY o.id,o.partner_id,o.size,o.state,l.grade_id,s.name
                    
        """
        return group_by_str


    @api.model_cr
    def init(self):
        # self._table = mill_order_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s
            WHERE o.state = 'draft' and l.order_id is not NULL
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

