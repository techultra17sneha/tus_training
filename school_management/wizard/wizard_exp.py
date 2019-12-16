from odoo import models,fields,api


class WizarExample(models.TransientModel):
    _name = "wizard.example"

    name = fields.Char('Name')
    rank = fields.Float('Rank')
    emp_type = fields.Selection([('all','ALL'),('individual','Individual')], string="Type")
    emp_id = fields.Many2one('hr.employee', string="Employee")

    def change_rank(self):
        for i in self:
            self.env[self._context.get('active_model')].browse(self._context.get('active_ids')).write({'overall_rank':i.rank})
            data = {
                'form': {
                    # 'start_date': start_date,
                    # 'end_date': end_date,
                    # 'records': rec_list
                },
            }
            data['form'].update(self.read([])[0])
            return self.env.ref('school_management.demo_qweb_report').report_action(self, data=data)

    @api.multi
    def get_value(self):
        res = []
        total = []
        if self.hr_id and self.user_id:
            task_id = self.env['project.task'].search([('user_id', '=', self.emp_id.id)])
            if task_id:
                performance = 0.0
                res.append({'task': task_id.name, 'performance': task_id.performance, 'done_date': task_id.done_date})
        return res


    def print_report(self):
        emp_ids = []
        data = self.read()
        if self.emp_type == 'individual':
            rec = self.env['hr.employee'].search([('name', '=', self.emp_id.name)])
            emp_ids.append(rec)
        else:
            rec = self.env['hr.employee'].search([])
            emp_ids.append(rec)
        # data = {
        #         'ids': self.ids,
        #         'model': self._name,
        #         'form':data
        #     }

        data = {'docs': self, 'model': self._name, 'emp_ids': emp_ids}
        return self.env.ref('school_management.demo_report_parser').report_action(self)




        # print("datttttttttttttttttttttt", data)
        # return self.env.ref('school_management.demo_report_parser').report_action(
        #     self.search([('id', '=', self.id)]), data)


class Hr(models.Model):

    _inherit='hr.employee'

    def get_details(self):
        rec = []
        record = self.search([])
        for i in record:
            rec.append(i.name)
        return rec



