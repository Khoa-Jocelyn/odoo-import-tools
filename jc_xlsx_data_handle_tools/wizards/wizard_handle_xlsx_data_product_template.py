import base64
from io import BytesIO
import xlsxwriter
from xlrd import open_workbook
from odoo import models,  _
from odoo.exceptions import ValidationError


class WizardHandleXlsxDataProductTemplate(models.TransientModel):
    _name = 'wizard.handle.xlsx.data.product.template'
    _inherit = 'wizard.handle.xlsx.data.mixin'
    _description = 'Wizard To Handle XLSX. Product Template Data'

    def action_export_xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/tools/%d/xlsx' % self.id,
        }

    def _handle_xlsx_data(self):
        self.ensure_one()
        file_contents = base64.b64decode(self.input_file)
        workbook = open_workbook(file_contents=file_contents)
        sheet = workbook.sheet_by_index(0)
        if sheet.nrows < 2:
            raise ValidationError(_("Your *.xlsx file has less values than expected!"))
        try:
            new_xlsx_values = {}
            for row in range(1, sheet.nrows):
                key = tuple([sheet.col_values(col)[row].strip() for col in range(sheet.ncols - 1)])
                if key not in new_xlsx_values:
                    new_xlsx_values[key] = [sheet.row_values(row)[-1].strip()]
                else:
                    new_xlsx_values[key].append(sheet.row_values(row)[-1].strip())
            new_xlsx_data = {'thead': sheet.row_values(0), 'tbody': new_xlsx_values}
            return new_xlsx_data
        except Exception as e:
            raise ValidationError(_("Your *.xlsx file does not following correct format! It created an error: %s") % e.args[0])

    def _create_xlsx_file(self):
        self.ensure_one()
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        self._generate_xlsx(workbook, self._handle_xlsx_data())
        workbook.close()
        file_data.seek(0)
        return file_data

    def _generate_xlsx(self, workbook, new_xlsx_values):

        xlsx_thead_data = new_xlsx_values['thead']
        xlsx_tbody_data = new_xlsx_values['tbody']

        # Create an new xlsx file and add a worksheet.
        worksheet = workbook.add_worksheet()

        # Set dimension for column and Format cells:
        worksheet.set_default_row(30)
        worksheet.set_column(0, 0, 50)
        worksheet.set_column(1, 1, 50)
        worksheet.set_column(2, 2, 50)
        worksheet.set_column(3, 3, 50)

        thead_format = workbook.add_format({
            'bold': True,
            'valign': 'vcenter',
            'font_size': 11,
            'font_name': 'Calibri',
        })

        tbody_format = workbook.add_format({
            'border': 1,
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
        })

        # Write table header
        worksheet.write('A1', xlsx_thead_data[0], thead_format)
        worksheet.write('B1', xlsx_thead_data[1], thead_format)
        worksheet.write('C1', xlsx_thead_data[2], thead_format)
        worksheet.write('D1', xlsx_thead_data[3], thead_format)

        row = 1
        # Insert values in columns
        for key, value in xlsx_tbody_data.items():
            worksheet.write(row, 0, key[0], tbody_format)
            worksheet.write(row, 1, key[1], tbody_format)
            worksheet.write(row, 2, key[2], tbody_format)
            worksheet.write(row, 3, ','.join(set(value)), tbody_format)
            row += 1
