# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    company_type = fields.Selection(string='Company Type',
        selection=[('person', 'Individual'), ('company', 'Company')])
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name') 
    gender = fields.Selection(string='Gender', 
                            selection=[
                                        ('male', 'Male'),
                                        ('female', 'Female'),
                                        ('notsay', 'Rather Not Say')
                                        ])
    nationality = fields.Many2one('res.country', string='Nationality')
    family_members = fields.Integer('Family members')
    estimated_annual_income = fields.Char('Estimated Annual Income')
    prior_agreed_fees = fields.Char('Prior Agreed Fees as per contract')
    start_contract_date = fields.Date('Start Date of Contract')
    expiry_contrat_date = fields.Date('Expiry Date of Contract')
    employment_status = fields.Selection([
                                ('', ''),
                                ('partner', 'Business Partner'),
                                ('contract1099', 'Contract 1099'),
                                ('fullw2', 'Full time W2'),
                                ('partw2', 'Part time W2'),
                                ('self', 'Self Employee'),
                                ('student', 'Student'),
                                ('unemployee', 'Unemployee'),
                                ('other', 'Other'),
                                ])
    nature_of_job = fields.Selection([
                                ('', ''),
                                ('aviation', 'Aviation'),
                                ('businessindustry', 'Business Industry'),
                                ('construction', 'Construction'),
                                ('education', 'Education'),
                                ('homebusiness', 'Home Business'),
                                ('manufacture', 'Manufacture'),
                                ('military', 'Military'),
                                ('nationalsecurity', 'National Security'),
                                ('publicsafety', 'Public Safety'),
                                ('publichealth', 'Public Health'),
                                ('retailstore', 'Retail Store'),
                                ('self', 'Self'),
                                ('warehouse', 'Warehouse'),
                                ('Other', 'Other'),
                                ])
    employer_name = fields.Char(string='Employer Name')
    interested_products = fields.Char(string='Interested Products')
    referral_name = fields.Char(string='Referral’s Name')
    birthdate = fields.Date(string='Birthday')
    #company registration form fields
    company_name = fields.Char(string='Company Name')
    company_address = fields.Text(string='Company Address')
    industry_sector = fields.Char('Industry Sector')
    industry_segment = fields.Char(string="Industry Segment")
    no_of_employees = fields.Selection([
                                        ('',''),
                                        ('1-4','1-4'),
                                        ('5-19','5-19'),
                                        ('20-49','20-49'),
                                        ('50-99','50-99'),
                                        ('100-499','100-499'),
                                        ('500-9999','500-9999')
                                        ])
    contact_name = fields.Char('Contact Name')
    contact_number = fields.Char('Contact Number')
    
