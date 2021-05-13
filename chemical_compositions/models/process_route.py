from odoo import tools
from odoo import api, fields, models


class ProcessRoute(models.Model):
    _name = "process.route"
    _desription  = "Process Route"


    name = fields.Char('Route')