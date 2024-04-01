# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields


# inherit res.partner and add new fields, for sign up form to create partner in contact as individual or company...
class ResPartner(models.Model):
    _inherit = 'res.partner'

    #individual registration form fields
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name') 
    gender = fields.Selection(string='Gender', 
                            selection=[
                                        ('male', 'Male'),
                                        ('female', 'Female'),
                                        ('rather not say', 'Rather not say')
                                        ])
    nationality = fields.Many2one('res.country', string='Nationality')
    employment_status = fields.Char(string="Current Employment Status")
    employer_name = fields.Char(string='Employer Name')
    nature_of_job = fields.Selection([
                                    ('', ''), 
                                    ('it', 'IT'), 
                                    ('retail', 'Retail'), 
                                    ('marketing', 'Marketing'), 
                                    ('construction', 'Construction'), 
                                    ('self', 'Self')
                                    ])
    industry_segment = fields.Char(string="Industry Segment")
    intrested_fields = fields.Char(string='Interested Fields')
    referral_name = fields.Char(string='Referral’s Name')
    birthdate = fields.Date(string='Birthday')

    #company registration form fields
    company_name = fields.Char(string='Company Name')
    company_address = fields.Text(string='Company Address')  
    no_of_employees = fields.Selection([
                                        ('',''), 
                                        ('>20','>20'), 
                                        ('20-50','20-50'), 
                                        ('50-70','50-70'), 
                                        ('70-100','70-100')
                                        ])
    industry_sector = fields.Char('Industry Sector')
    course_id = fields.Many2one('slide.channel', string='Select Course')
    no_registered_employee = fields.Integer('No of Employee to be Registred')
    contract_term = fields.Selection([
                                    ('',''), 
                                    ('6 months','6 Months'), 
                                    ('1 year','1 Year'), 
                                    ('2 Year','2 Year'), 
                                    ('>2 years','>2 Years')
                                    ])
    contact_name = fields.Char('Contact Name')
    contact_number = fields.Char('Contact Number')
    designation = fields.Char('Designation')
    susbcription_fee = fields.Char('Estimated Subscription Fee')
    prior_agreed_fees = fields.Char('Prior Agreed Fees as per contract')
    start_contract_date = fields.Date('Start Date of Contract')
    expiry_contrat_date = fields.Date('Expiry Date of Contract')
    