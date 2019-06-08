from odoo import tools
from odoo import api, fields, models


class TestReport(models.Model):
    _name = "test.report"
    _description = "Test Report"
    _auto = False
    
    date = fields.Date('Date',default = fields.Date.today)
    grade_id = fields.Many2one('material.grade','Grade')
    supplier_id = fields.Many2one('res.partner','Supplier')
    
    def _select(self):
        select_str = """
            select 
                min(l.id) as id,
                date,
                grade_id,
                supplier_id
        """ 
        return select_str
    
    def _from(self):
        from_str = """
            test_line  l
        """
        return from_str
        
    def _group_by(self):
        group_by_str = """
            GROUP BY date,
                    grade_id,
                    supplier_id
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

