from odoo import api, fields, models, _


class Test(models.AbstractModel):
    _name = 'report.school_management.test_info'

    @api.model
    def get_report_values(self, docids, data):
        print("docids----------------",data)
