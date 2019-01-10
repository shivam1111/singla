from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class ProductionOrder(models.Model):
    _name="production.order"