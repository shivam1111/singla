from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    is_broker = fields.Boolean('Broker')
