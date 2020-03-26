from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class ChemicalComposition(models.Model):
    _inherit = "chemical.composition"
    _description = "Chemical Composition Stock"
    
    @api.onchange('heat_id')
    def onchange_heat_id(self):
        data = []
        data1 = []
        for i in self.heat_id.line_ids:
            data.append((0,0,{'element_id':i.element_id,'min_val':i.min_val,'max_val':i.max_val,'actual_val':i.actual_val}))
        for i in self.heat_id.inclusion_rating_ids:
            data1.append((0,0,{'type':i.type,'thin':i.thin,'thick':i.thick}))
        self.heat_no = self.heat_id.name
        self.line_ids = data            
        self.inclusion_rating_ids = data1
        return
    
    heat_id = fields.Many2one('heat.heat','Select Heat No.')
    