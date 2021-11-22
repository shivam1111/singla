from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class MillOrder(models.Model):
    _inherit = "mill.order"
    _description = "Mill Order"

    purchase_id = fields.Many2one('mill.purchase.order','Purchase Order')