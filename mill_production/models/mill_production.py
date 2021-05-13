from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo import SUPERUSER_ID

class StockLine(models.Model):
    _inherit = "stock.line"
    _description = "Stock Line (Production)"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('stock.line.production') or _('New')
        result = super(StockLine, self).create(vals)
        return result        

    @api.onchange('pcs','kg_per_pc')
    def _compute_qty(self):
        self.qty  = -(self.kg_per_pc * self.pcs)/1000
    
    @api.one
    @api.depends('kwh_closing','kwh_opening')
    def _compute_units(self):
        self.units = (self.kwh_closing - self.kwh_opening)*10

    @api.one
    @api.depends('scrap','qty')
    def _compute_scrap(self):
        try:
            self.scrap_percentage = (self.scrap*100)/(1000*self.qty)
        except ZeroDivisionError:
            self.scrap_percentage = 0.00
        
    name = fields.Char('Name')
    sequence = fields.Integer('sequence', help="Sequence for the handle.",default=10)
    size_id = fields.Many2one('size.size',string  = "Size")
    batch = fields.Float('No. of Batch',help = "Dhakku")
    kg_per_pc = fields.Float('Kg/pc')
    production_id = fields.Many2one('mill.production','Production',ondelete='cascade')
    kwh_opening = fields.Float('KWH Op.')
    kwh_closing = fields.Float('KWH Cl.')
    kva_opening = fields.Float('KVA Op.')
    kva_closing = fields.Float('KVA Cl.')
    units = fields.Float('Units',compute = "_compute_units")
    scrap = fields.Float('Scrap')
    scrap_percentage = fields.Float('Scrap%',compute = "_compute_scrap")
    production_line_id = fields.Many2one('production.order.line','Prooduction Line',help = "This field stores the planned productio line")
    stock_id = fields.Many2one('stock.line','Stock Line')
    sale = fields.Float('Sale')
    
    

class MillProduction(models.Model):
    _name = 'mill.production'
    _description = "Mill Production Register"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    @api.one
    @api.depends('production_line_ids','production_line_ids.qty')
    def _compute_total_production(self):
        total = 0.00
        for i in self.production_line_ids:
            total = total+i.qty
        self.total_production = -total
        
    @api.one
    @api.depends('coal','total_production')
    def _compute_coal_mt(self):
        total = 0.00
        try:
            self.coal_mt = self.coal/self.total_production
        except ZeroDivisionError:
            self.coal_mt = 0.00
    
    @api.multi
    def write(self,vals):
        if self.env.user.has_group('mill_order.group_dispatch_manager')  and self.env.user.id != SUPERUSER_ID :
            raise UserError(_('You are not allowed to make changes to this record'))
        return super(MillProduction, self).write(vals)
    
    @api.model
    def create(self, vals):
        if self.env.user.has_group('mill_order.group_dispatch_manager')  and self.env.user.id != SUPERUSER_ID :
            raise UserError(_('You are not allowed to create this record'))
        vals['name'] = self.env['ir.sequence'].next_by_code('mill.production') or _('New')
        result = super(MillProduction, self).create(vals)
        return result    
    
    @api.one
    @api.depends('total_production','production_line_ids.scrap')
    def _compute_scrap(self):
        total = 0.00
        for i in self.production_line_ids:
            total = total+i.scrap 
        self.total_scrap = total       
        try:
            self.scrap_percentage = (total*100)/(1000*self.total_production)
        except ZeroDivisionError:
            self.scrap_percentage = 0.00
    
    @api.one
    @api.depends('production_line_ids','production_line_ids.units','total_production')
    def _compute_units(self):
        total = 0.00
        for i in self.production_line_ids:
            total = total+i.units        
        self.total_units = total
        try:
            self.units_per_mt = total/self.total_production
        except ZeroDivisionError:
            self.units_per_mt = 0.00
        try:
            self.kwh_mt = total/self.total_production        
        except ZeroDivisionError:
            self.kwh_mt = 0.00

    @api.one
    @api.depends('png_units_opening','png_units_closing')
    def _compute_png_units(self):
        self.png_net = self.png_units_closing - self.png_units_opening



    name = fields.Char('Name',default = '/',required = True)
    date = fields.Date('Date',required=True,default = fields.Date.today)
    total_production = fields.Float('Total Production',compute = "_compute_total_production",store=True)
    remarks = fields.Text('Remarks')
    production_line_ids = fields.One2many('stock.line','production_id','Production Lines')
    md_mt = fields.Float('MD/MT')
    coal = fields.Float('Total Coal')
    coal_mt = fields.Float('Coal/MT',compute = "_compute_coal_mt",store=True)
    total_scrap = fields.Float('Total Scrap',compute = "_compute_scrap",store=True )
    scrap_percentage = fields.Float('Scrap%',compute = "_compute_scrap")
    hours = fields.Float('Total Hours')
    furnace_kara = fields.Float('Furnace Kara')
    mill_kara = fields.Float('Mill Kara')
    miss_roll = fields.Text('Miss Roll')
    total_units = fields.Float("Total Units Consumed",compute = "_compute_units",store=True)
    units_per_mt = fields.Float('Units/MT',compute = '_compute_units')
    kwh_mt = fields.Float('KWH/MT',compute = '_compute_units' )
    size_id = fields.Many2one('size.size',related= "production_line_ids.size_id",string = "Size")
    water_units_opening = fields.Float('Water Units Opening')
    water_units_closing  = fields.Float('Water Units Closing')
    solar_units_opening_kwh = fields.Float('Solar Units Opening (KWH)')
    solar_units_closing_kwh = fields.Float('Solar Units Closing (KWH)')
    solar_units_opening_kvah = fields.Float('Solar Units Opening (KVaH)')
    solar_units_closing_kvah = fields.Float('Solar Units Closing (KVaH)')
    png_units_opening = fields.Float('PNG Opening')
    png_units_closing = fields.Float('PNG Closing')
    png_net = fields.Float("Net PNG",compute = '_compute_png_units',store=True)
    