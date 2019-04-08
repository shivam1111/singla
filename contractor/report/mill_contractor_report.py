from odoo import tools
from odoo import api, fields, models


class MillContractorReport(models.Model):
    _name = "mill.contractor.report"
    _description = "Mill Contractor Report"
    _auto = False
    
    name = fields.Char('Name',default = "/")
    date = fields.Date('Date',default = fields.Date.today)
    qty = fields.Float('Qty')    
    contractor_id = fields.Many2one('mill.contractor','Contractor')
    to_pay = fields.Float('To Pay')
    partner_id = fields.Many2one('res.partner','Partner')
    
    def _select(self):
        select_str = """
            select 
                min(l.id) as id,
                name,
                date,
                SUM(qty) as qty,
                SUM(to_pay)  as to_pay,
                partner_id,
                contractor_id
        """ 
        return select_str
    
    def _from(self):
        from_str = """
            contractor_mt_line  l
        """
        return from_str
        
    def _group_by(self):
        group_by_str = """
            GROUP BY name,
                    partner_id,
                    contractor_id,
                    date
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

