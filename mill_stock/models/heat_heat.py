from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class CompositionLine(models.Model):
    _inherit = "composition.line"
    _description = "Stock Composition Line"
    
    heat_id = fields.Many2one('heat.heat','Heat')

class Heat(models.Model):
    _name = 'heat.heat'
    _description = "Heats"

    @api.onchange('grade_id')
    def _onchange_grade_id(self):
        data = []
        line_ids = []
        # First check if the record is being created or grade_id value if being changed
        if self._context.get('onchange',False):
            # This means the grade_id field value is being changed
            line_ids = self.grade_id and self.grade_id.line_ids or []
        elif self.stock_line_id.purchase_id:
            line_ids = self.stock_line_id.purchase_id.line_ids
        elif self.grade_id:
            line_ids = self.grade_id.line_ids
        for i in line_ids:
            data.append((0,0,{'element_id':i.element_id,'min_val':i.min_val,'max_val':i.max_val}))
        self.line_ids = data            

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('heat.heat') or _('New')
        result = super(Heat, self).create(vals)
        return result
        
    
    name = fields.Char('Name',default = '/',required = True)
    furnace_heat_no = fields.Char('Furnace Heat No.',required = True)
    date = fields.Char('Date Rcvd',required=True,default = fields.Date.today)
    truck_no = fields.Char('Truck No.',related = "stock_line_id.truck_no")
    stock_line_id = fields.Many2one('stock.line','Stock Line')
    grade_id = fields.Many2one(string = "Grade",store=True,related = "stock_line_id.grade_id")
    line_ids = fields.One2many('composition.line','heat_id','Chemical Composition Report')
    surface_inspection = fields.Boolean('Surface Inspection')
    size = fields.Many2one('ingot.size','Size')
    supervisor_id = fields.Many2one('res.users','Supervisor',default = lambda self:self.env.user)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    