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
    _description = "Inclusion Rating Line"
    
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
    
    @api.depends('line_ids','line_ids.element_id','line_ids.actual_val')
    def _compute_carbon_equivalence(self):
        ce = 0.00
        ce_elem = ['C','Mn']
        nicrmo_elem = ['Ni','Cr','Mo']
        nicrmo = 0.00
        try:
            for tc in self:
                for l in tc.line_ids:
                  if l.element_id.code == 'C':
                      ce += float(l.actual_val)
                      ce_elem.remove('C')
                  elif l.element_id.code == 'Mn':
                      ce += float(l.actual_val)/6.00
                      ce_elem.remove('Mn')
                  elif l.element_id.code == 'Ni':
                      nicrmo += float(l.actual_val)
                      nicrmo_elem.remove('Ni')
                  elif l.element_id.code == 'Mo':
                      nicrmo += float(l.actual_val)
                      nicrmo_elem.remove('Mo')  
                  elif l.element_id.code == 'Cr':
                      nicrmo += float(l.actual_val)
                      nicrmo_elem.remove('Cr')
        except ValueError:
            # Do nothing
            return
        if len(ce_elem) == 0:
            self.carbon_equivalence = round (ce + 1.00/20.00,2)
        if len(nicrmo_elem) == 0:
            self.nicrmo = round(nicrmo,2)               
    
    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner','Partner')
    no_of_pieces = fields.Float('Number of Pieces')
    date = fields.Date('Date',default = fields.Date.today)
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
    min_hardness = fields.Char("Min. Hardness",default = "255")
    max_hardness = fields.Char("Max. Hardness",default = "280")
    complete_decarb = fields.Float('Complete Decarb')
    partial_decarb = fields.Float('Partial Decarb')
    grain_size = fields.Float('Grain Size')
    qty = fields.Char('Qty')
    ultimate_tensile_strength = fields.Float('Ultimate Tensile Strength (N/mm2)')
    yield_strength = fields.Float('Yield Strength (N/mm2)')
    elongation = fields.Float('Elongation %')
    reduction_ratio = fields.Char('Reduction Ratio')
    spark_test = fields.Boolean('Spark Test',default=False)
    is_xrf = fields.Boolean ('XRF Test',default=True)
    is_ut = fields.Boolean('UT Test')
    is_mpi = fields.Boolean('MPI')
    carbon_equivalence = fields.Float('Carbon Equivalence',default = 0.00,help = "%C + (%Mn/6) + 1/20",compute = '_compute_carbon_equivalence')
    nicrmo = fields.Float('Ni+Cr+Mo',compute = '_compute_carbon_equivalence')
    surface_inspection = fields.Selection([('ok','Ok'),('dentfree','Free from Dent')],default = 'dentfree')

    