from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class LengthDetail(models.Model):
    _name = "length.detail"
    _description  = "Length Details"
    
    name = fields.Char("Length")
    no_of_pcs = fields.Float('No. of Pcs')
    composition_id = fields.Many2one('chemical.composition','Composition')

class InclusionRatingLine(models.Model):
    _name = "inclusion.rating.line"
    _description = "Inclusion Ratio Line"
    
    type = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D')],string = "Inclusion Type")
    thin = fields.Char('Thin')
    thick = fields.Char('Thick')
    composition_id = fields.Many2one('chemical.composition','Composition')

class ChemicalElement(models.Model):
    _name = "chemical.element"
    _description = "Chemical Element"
    
    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)

class CompositionLine(models.Model):
    _name = "composition.line"
    _description = "Composition Line"
    
    element_id = fields.Many2one('chemical.element','Element',required=True)
    min_val = fields.Char('Min')
    max_val = fields.Char('Max')
    actual_val = fields.Char('Actual')
    furnace_val = fields.Char('Furnace Report')
    composition_id = fields.Many2one('chemical.composition','Composition')
    grade_id = fields.Many2one('material.grade','Material Grade')
    sequence = fields.Integer('Sequence') 

class ChemicalComposition(models.Model):
    _name = "chemical.composition"
    _description = "Chemical Composition"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
     
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('chemical.composition') or _('New')
        result = super(ChemicalComposition, self).create(vals)
        return result    
   
    @api.onchange('grade_id') # if these fields are changed, call method
    def _chage_grade_id(self):
        data = []
        for i in self.grade_id.line_ids:
            data.append((0,0,{'element_id':i.element_id,'min_val':i.min_val,'max_val':i.max_val}))
        self.line_ids = data
    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner','Partner')
    no_of_pieces = fields.Float('Number of Pieces')
    date = fields.Date('Date',default = fields.Date.today())
    truck_no = fields.Char('Vehicle No.')
    heat_no = fields.Char('Heat No.')
    grade_id = fields.Many2one('material.grade','Grade')
    size = fields.Char('Size')
    color_code = fields.Char('Color Code')
    invoice_no = fields.Char('Invoice No.')
    line_ids = fields.One2many('composition.line','composition_id','Composition Line')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    inclusion_rating_ids = fields.One2many('inclusion.rating.line','composition_id','Inclusion Rating')
    length_detail_ids = fields.One2many('length.detail','composition_id','Length Details')
    rate_extra = fields.Float('Rate Extra',help = "Basic + Extra Rate")
    attested = fields.Boolean('Attested',default=True)
    min_hardness = fields.Char("Min. Hardness",default = "255")
    max_hardness = fields.Char("Max. Hardness",default = "280")
    complete_decarb = fields.Float('Complete Decarb')
    partial_decarb = fields.Float('Partial Decarb')
    grain_size = fields.Float('Grain Size')
    
    