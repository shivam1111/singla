from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class CompositionLine(models.Model):
    _inherit = "composition.line"
    
    purchase_order_id = fields.Many2one('mill.purchase.order',"Mill Purchase Order")