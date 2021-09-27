# -*- coding: utf-8 -*-
##############################################################################
#
#    India-GST
#
#    Merlin Tecsol Pvt. Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, models, fields, _
import logging,os
# Service A/C imports
# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
_logger = logging.getLogger(__name__)
GOOGLESHEET_URL = 'https://docs.google.com/spreadsheets/d/1D-euhy3H0koC6Cr-AX1CqSUkvD2CvwUeQ4vAkcUgw5o/edit#gid=149290768'
COMPANIES = [('SKG','SKG'),('FP','FP')]
col_field = ['company_name','po','vendor','item_code','uniparts_grade','grade','item_description','qty','rate','dispatch','balance','bill_details',
             'status','cancelled','remarks']

class WizardSheetRow(models.TransientModel):
    _name = "sheet.row"

    row = fields.Char('Row')
    company_name = fields.Selection(COMPANIES,string = "Company")
    po = fields.Char('PO')
    # vendor = fields.Char('Vendor')
    item_code = fields.Char('Item Code')
    uniparts_grade = fields.Char('Uniparts Grade')
    grade = fields.Char('Grade')
    item_description = fields.Char('Item Description')
    qty = fields.Char('Qty Ordered')
    rate = fields.Char('Rate')
    dispatch = fields.Char('Dispatch')
    balance = fields.Char('Balance')
    bill_details = fields.Char('Bill Details')
    status = fields.Boolean('Status')
    cancelled = fields.Boolean('Cancelled')
    remarks = fields.Char('Remarks')

class WizardGooleSpreadsheet(models.TransientModel):
    _name = 'google.spreadsheet'

    item_code = fields.Char('Item Code',required=True)
    status = fields.Boolean('Status')
    cancelled = fields.Boolean('Cancelled')
    line_ids = fields.Many2many('sheet.row','google_spreadsheet_sheet_row_rel','spreadsheet_id','row_id','Search Results',ondelete = 'cascade')
    all = fields.Boolean('All',help = "Get all lines whether status checked or not")

    @api.multi
    def fetch_query(self,vals):
        self.line_ids = [(6, 0, [])]
        # define the scope
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        if os.path.exists('credentials.json'):
            # add credentials to the account
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        else:
            return

        # authorize the clientsheet
        client = gspread.authorize(creds)
        # get the instance of the Spreadsheet
        sheet = client.open_by_url(GOOGLESHEET_URL)
        # By title
        worksheet = sheet.worksheet("Main Sheet")
        itemcode_rows = worksheet.findall(self.item_code.upper())
        rows_list = []
        for item in itemcode_rows:
            rows_list.append("%s:%s" % (item.row,item.row))
        if rows_list:
            records = []
            values_list = worksheet.batch_get(rows_list, value_render_option='UNFORMATTED_VALUE')
            for i,item in enumerate(values_list):
                record = dict(zip(col_field,item[0]))
                record.update({
                    'row':itemcode_rows[i].row
                })
                if self.all:
                    records.append(record)
                    self.line_ids += self.env['sheet.row'].create(record)
                elif record.get('status',False) == self.status and record.get('cancelled',False) == self.cancelled:
                    records.append(record)
                    self.line_ids += self.env['sheet.row'].create(record)

        return {
            "type": "ir.actions.do_nothing",
        }

