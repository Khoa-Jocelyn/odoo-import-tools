from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WizardHandleXlsxDataMixin(models.AbstractModel):
    _name = 'wizard.handle.xlsx.data.mixin'
    _description = 'Mixin Wizard To Handle XLSX Data'

    input_file = fields.Binary(string='Input File', required=True)

    def _get_file_name(self):
        return 'IMPORT_DATA'

    def _handle_xlsx_data(self):
        raise UserError(_('Could not make sense of the given file.\nDid you install the module to support this type of file ?'))

    def handle(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/tools/%d/xlsx' % self.id,
        }
