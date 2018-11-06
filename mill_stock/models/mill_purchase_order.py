from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _


class MillPurchaseOrder(models.Model):
    _inherit = 'mill.purchase.order'
    
    @api.one
    @api.depends('stock_line_ids','material_ordered')
    def _compute_stock_received(self):
        total = 0.00
        for i in self.stock_line_ids:
            total = total + i.qty
        self.material_received  = total

    @api.one
    @api.depends()
    def _compute_stock_balance(self):
        balance = self.material_ordered - self.material_received
        self.balance = max(balance,0)
        
    stock_line_ids = fields.One2many('stock.line','purchase_id','Stock')
    material_received = fields.Float('Material Qty Received',compute = "_compute_stock_received",store=True)
    balance = fields.Float('Balance',compute = "_compute_stock_balance")
    