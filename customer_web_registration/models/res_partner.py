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
                                        ('female', 'Female')
                                        ])
    nationality = fields.Many2one('res.country', string='Nationality')
    employment_status = fields.Char(string="Current Employment Status")
    employer_name = fields.Char(string='Employer Name')
    nature_of_job = fields.Selection([
                                    ('', ''), 
                                    ('it', 'IT'), 
                                    ('retail', 'Retail'), 
                                    ('marketing', 'Marketing'), 
                                    ('manufacture', 'Manufacture'), 
                                    ('construction', 'Construction'), 
                                    ('self', 'Self')
                                    ])
    industry_segment = fields.Char(string="Industry Segment")
    interested_products = fields.Char(string='Interested Products')
    referral_name = fields.Char(string='Referral’s Name')
    birthdate = fields.Date(string='Birthday')

    #company registration form fields
    company_name = fields.Char(string='Company Name')
    company_address = fields.Text(string='Company Address')  
    no_of_employees = fields.Selection([
                                        ('',''), 
                                        ('1-4','1-4'), 
                                        ('5-19','5-19'), 
                                        ('20-49','20-49'), 
                                        ('50-99','50-99'),
                                        ('100-499','100-499'),
                                        ('500-9999','500-9999')
                                        ])
    industry_sector = fields.Char('Industry Sector')
    carrier_id = fields.Many2one('slide.channel', string='Select Carrier')
    family_members = fields.Integer('Family members')
    contract_term = fields.Selection([
                                    ('',''), 
                                    ('1 time','1 time'), 
                                    ('1 year','1 Year'), 
                                    ('>1 years','>1 Years')
                                    ])
    contact_name = fields.Char('Contact Name')
    contact_number = fields.Char('Contact Phone')
    susbcription_fee = fields.Char('Estimated Subscription Fee')
    estimated_premium = fields.Integer('Estimated Premium')
    prior_agreed_fees = fields.Char('Prior Agreed Fees as per contract')
    start_contract_date = fields.Date('Start Date of Contract')
    expiry_contrat_date = fields.Date('Expiry Date of Contract')
    
