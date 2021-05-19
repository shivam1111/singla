from odoo import api, fields, models


# configuration for report
class resConfigSettings(models.TransientModel):
    _name ='report.creator.config.settings'
    _inherit = 'res.config.settings'
    
    @api.model 
    def _get_default_path(self):
        path_report_creator = self.env['ir.config_parameter'].get_param('path_file_store', default='')
        return path_report_creator
    
    
    file_store = fields.Char(string="File Store",default=_get_default_path)
    
#     set value for file_store
    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('path_file_store', (self.file_store or '').strip())#         
        
    def get_deault_path(self):
        path_report_creator = self.env['ir.config_parameter'].get_param('path_file_store', default='')
        return path_report_creator
     
#     return all values configuration
    def get_path(self):
        return self.get_deault_path()
     
     

