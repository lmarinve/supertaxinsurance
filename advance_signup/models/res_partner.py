# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

# inherit res.partner and add new fields, for sign up form to create partner in contact as individual or company...
class ResPartner(models.Model):
    _inherit = 'res.partner'

    #individual registration form fields
    gender = fields.Selection(string='Gender', 
                            selection=[
                                        ('male', 'Male'),
                                        ('female', 'Female')
                                        ])
    tobacco = fields.Boolean(string="Tobacco User")
    date = fields.Date(string='Birthday')
    age = fields.Integer(string='Age')
    weight = fields.Integer(string='Weight')
    height = fields.Integer(string='Height')
    civil_status = fields.Selection(string='Civil Status', 
                            selection=[
                                        ('single', 'Single'),
                                        ('household', 'Household'),
                                        ('married', 'Married'),
                                        ('separated', 'Separated'),
                                        ('divorced', 'Divorced')
                                        ])
    dependents = fields.Integer(string="Dependents")
    place_of_birth = fields.Char(string='Place of Birth')
    nationality = fields.Many2one('res.country', string='Nationality')
    license_no = fields.Char(string='Driver License or ID')
    license_exp = fields.Date('ID Expiration')
    passport_no = fields.Char(string='Passport number')
    passport_exp = fields.Date('Passport Expiration')
    permit_no = fields.Char(string='Work Permit')
    permit_exp = fields.Date('Work Permit Expiration')
    employment_status = fields.Selection(string="Employment Status",
                            selection=[
                                        ('w2', 'W2'),
                                        ('1099', '1099'),
                                        ('self', 'Self'),
                                        ('student', 'Student'),
                                        ('unemployee', 'Unemployee')
                                        ])
    income = fields.Integer(string="household income AGI")
    job_title = fields.Char(string='Job Title')
    business_category = fields.Many2one('adv.business.category', string="Business Category")
    business_activity = fields.Many2one('adv.business.activity', string="Business Activity")

    #company registration form fields
    no_of_employees = fields.Selection([
                                        ('',''),
                                        ('1-4','1-4'),
                                        ('5-19','5-19'),
                                        ('20-49','20-49'),
                                        ('50-99','50-99'),
                                        ('100-499','100-499'),
                                        ('500-9999','500-9999'),
                                        ('10000-100000','10000-100000')
                                        ])


    @api.onchange('business_category')
    def on_change_category(self):
        _logger.info("***********************")
        _logger.info("******* business_category *******")
        _logger.info(self.business_category.id)
        _logger.info("***********************")
        if self.business_category:
            ids = self.env['adv.business.activity'].search([('category_id', '=', self.business_category.id)])
        return {
            'domain': {'business_activity': [('id', 'in', ids.ids)],}
        }
