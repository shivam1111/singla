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
    tensile_strength_min = fields.Float('Min. Tensile Strength')
    tensile_strength_max = fields.Float('Max. Tensile Strength')
    yield_strength_min = fields.Float('Min. Yield Strength')
    yield_strength_max = fields.Float('Max. Yield Strength')
    elongation_min = fields.Float("Min. Elongation")
    elongation_max = fields.Float("Max. Elongation")
    mechanical_properties = fields.Boolean('Mechanical Properties')
    hardness_min = fields.Float('Min. Hardness')
    hardness_max = fields.Float("Max. Hardness")
    decarb_min = fields.Float('Min. Decarb')
    decarb_max = fields.Float('Max. Decarb')