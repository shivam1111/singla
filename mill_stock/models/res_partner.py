from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _


class ReportBrokerageReport(models.AbstractModel):
    _name = 'report.mill_stock.brokerage_report'

    @api.model
    def render_html(self, docids, data=None):
        docs = self.env['stock.line'].search([('id','=',data['doc_ids'])],order='date asc')
        docargs = {
           'doc_ids': data['doc_ids'],
           'doc_model': data['doc_model'],
           'docs':docs,
           'broker_name': data['broker_name'],
        }
        return self.env['report'].render('mill_stock.brokerage_report', docargs)

class ResPartner(models.Model):
    _inherit = "res.partner"

    from_dt_brokerage = fields.Date('From')
    to_dt_brokerage = fields.Date('To')

    @api.multi
    def print_brokerage(self):
        stock_line = self.env['stock.line'].search([('purchase_id.broker_id','=',self.id),
                                                    ('date','>=',self.from_dt_brokerage),
                                                    ('date','<=',self.to_dt_brokerage),
                                                    ('state','!=','cancel'),
                                                    ('type','in',['purchase','trade'])
                                                    ])
        data = {
            'doc_model': 'stock.line',
            'doc_ids': stock_line.ids,
            'broker_name': self.name,
        }
        return self.env['report'].get_action(self,'mill_stock.brokerage_report',data)

    # @api.model
    # def render_html(self, docids, data=None):
    #     docargs = data
    #     return self.env['report'].render('sales_report.report_salesperson', docargs)
