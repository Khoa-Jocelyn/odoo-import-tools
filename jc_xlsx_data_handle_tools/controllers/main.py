from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import content_disposition, request


class StockReportController(http.Controller):

    @http.route('/tools/<int:id>/xlsx', type='http', auth='user')
    def download_xlsx_file(self, id, **kwargs):
        wizard = request.env['wizard.handle.xlsx.data.product.template'].browse(id)
        if not wizard.exists():
            raise AccessError(_("Record not found: id: %s, uid: %s")) % (id, request.env.user.id)

        output_file = wizard._create_xlsx_file()
        output_filename = wizard._get_file_name() + '.xlsx'
        content_length = len(output_file.getvalue())
        http_header = [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Length', content_length),
            ('Content-Disposition', content_disposition(output_filename))
        ]

        return request.make_response(output_file, headers=http_header)
