# -*- coding: utf-8 -*-
import datetime
from lxml import etree
from odoo.exceptions import ValidationError
from odoo import models, fields, api

class school_management(models.Model):
    _name = 'school_management.school_structure'
    _description = ""
    _rec_name = 'value'

    name = fields.Char()
    value = fields.Integer()
    description = fields.Text()
    created_on = fields.Date(string="Created On")
    is_class_full = fields.Boolean(string="Class")
    last_admission = fields.Datetime()
    class_image = fields.Binary()
    overall_rank = fields.Float()
    is_boolean_ticked = fields.Boolean('Ticked', default=False)
    standard = fields.Selection([('primary', 'Primary'), ('secondary', 'Secondary'), ('higher', 'Higher')], string="Standard", default='higher')
    states = fields.Selection([('new', 'New'), ('submit', 'Submitted'), ('done', 'Done')],
                              string='State', default='new')
    employee_id = fields.Many2one('hr.employee', string="Teacher")
    subject_id = fields.Many2one('school.subject')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Value cannot be duplicate in records. Please assign another value.')
    ]

    @api.constrains('value')
    def check_age(self):
        """
        Added a validation method to check the age of an employee to be 18
        ------------------------------------------------------------------
        @param self : object pointer
        """
        for emp in self:
            if emp.value == 12:
                raise ValidationError('There are duplicate values.')

    # @api.multi
    def action_change_color(self):
        # for rec in self:
        self.is_boolean_ticked = True
        return True

class HrDepartment(models.Model):
    _inherit = "hr.department"



class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_teacher = fields.Boolean('Teacher')
    subject_id = fields.One2many('school.subject', 'teacher_id', "Subject")

    @api.model
    def default_get(self, fields):
        res = super(HrEmployee, self).default_get(fields)
        if res.get('certificate') == 'other':
            dept = self.env['hr.department'].search([('name', '=', 'Management')], limit=1)
            res['department_id'] = dept.id
        return res

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     """
    #     Overridden fields_view_get method to change some attribute in the views
    #     -----------------------------------------------------------------------
    #     @param self : object pointer
    #     @param view_id : the id of view
    #     @param view_type : the type of the view
    #     @param toolbar : toolbar on the form view and tree view #Actions/Print/Attachments
    #     @param submenu : deprecated
    #     """
    #     res = super(HrEmployee, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     # print (">>>>res>>>>>>>>>>>>>>>>",res)
    #     #         print "RES",res
    #     # Convert the string arch to dom
    #     print ("etreeeeeeeeeee----------------------",etree)
    #     dom = etree.XML(res['arch'])
    #     # print ("dom-----------",dom)
    #     # Using the env variables cr, uid, context
    #     #         print "SELF CTX",self._context
    #     #         print "SELF CR",self._cr
    #     #         print "SELF UID",self._uid
    #     cr, uid, context = self.env.args
    #     #         print "CR",cr
    #     #         print "UID",uid
    #     #         print "CTX",context
    #     # Checking the context passed from action
    #     # print ("self._context---------------",self._context)
    #     if self._context.get('model', 'hr.employee'):
    #         # Searching the node of the field
    #         # Here we have searched dept_id field
    #         print ("dom.xpath()////////////////////",dom.xpath("//field[@name='department_id']"))
    #         for node in dom.xpath("//field[@name='department_id']"):
    #             # Setting the attribute to the node
    #             # Which is setting up attribute domain to the field
    #             # Here we are adding domaiin on department field
    #             node.set("domain", "[('name','ilike','Res')]")
    #     else:
    #         for node in dom.xpath("//field[@name='gender']"):
    #             node.set("modifiers", '{"invisible":true}')
    #     # Convert the dom back to string and replace it with the old arch
    #     res['arch'] = etree.tostring(dom)
    #     #         print "RES",res['arch']
    #     return res

    @api.multi
    def name_get(self):
        """
        Overridden name_get method to display name and code both in relational fields
        -----------------------------------------------------------------------------
        @param self : object pointer
        @return : A list containing tuples where each tuple will
                  have id and the generated string
        """
        res = []
        for dept in self:
            disp_str = ''
            if dept.department_id:
                disp_str += dept.name + " - " + dept.department_id.name
            res.append((dept.id, disp_str))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        Overridden name_search method to search departments with name and code both
        ---------------------------------------------------------------------------
        @param self : object pointer
        @param name : the string that is typed in search of m2o
        @param args : any domain passed on many2one
        @param operator : the operator to be used for searching
        @param limit : no of records to be displayed.
        """
        # This will be the string that is typed in the many2one field
        # This will be the domain that is passed on the many2one field
        # This is the default operator
        # This is the limit of the records
        # If no args is there create one.
        if not args:
            args = []
        if name:
            # Search the records with name or code both
            args += ['|', ('department_id.name', operator, name), ('work_phone', operator, name)]
        depts = self.search(args, limit=limit)
        return depts.name_get()

    @api.onchange('certificate')
    def onchange_certificate(self):
        if self.certificate == 'master':
            print("//\n>>>>>>>>>>>>", self.certificate)
            self.department_id = self.env['hr.department'].search([('name', '=', 'Management')], limit=1)
        if self.certificate == 'other':
            print("//\n>>>>>>>>>>>>", self.certificate)
            self.department_id = self.env['hr.department'].search([('name', '=', 'Professional Services')], limit=1)
        if self.certificate == 'bachelor':
            print("//\n>>>>>>>>>>>>", self.certificate)
            self.department_id = self.env['hr.department'].search([('name', '=', 'Research & Development')], limit=1)


class Subjects(models.Model):
    _name = "school.subject"

    name = fields.Char('Subject Name')
    teacher_id = fields.Many2one('hr.employee', string="Teacher")
    department_id = fields.Many2one('hr.department', related="teacher_id.department_id", readonly=False, string="Department")


class Student(models.Model):
    _name = "school.student"
    _order = "name"

    name = fields.Char('Name')
    standard = fields.Integer('Standard')
    subject_ids = fields.Many2many('school.subject', 'student_id', 'subject_id', string="Subjects")
    dob = fields.Date('Date of Birth')
    age = fields.Integer(compute="_compute_age", string="Age")

    @api.depends('dob')
    def _compute_age(self):
        if self.dob:
            today = datetime.date.today()
            age = today - self.dob
            self.age = age.days / 365


class Sports(models.Model):
    _name = "school.sport"

    name = fields.Char('Name')
    coach_id = fields.Many2one('hr.employee')



class SchoolCompose(models.TransientModel):
    _name = 'school.compose.inherit'
    _inherits = {'res.partner': 'partner_id'}


    name = fields.Char('Name')
    code = fields.Char('code')
    partner_id = fields.Many2one('res.partner',ondelete='restrict', auto_join=True,string='Related Partner')



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    code = fields.Char('Code')

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        res = super(SaleOrder, self)._amount_all()
        for rec in self:
            rec.code = 'Test'
        print("::::::::::::::::::::::::::::::::::::",res)