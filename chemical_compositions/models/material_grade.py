from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class MaterialGrade(models.Model):
    _inherit= "material.grade"
    _description = "Material Grade"
    
    line_ids = fields.One2many('composition.line','grade_id','Composition Line')
    price_extra = fields.Float('Extra Price')
    remarks = fields.Text('Remarks')
    name_str = fields.Char('Print Name')