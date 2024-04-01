# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


# inherit crm.lead model and add new fields, for contact us page
class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"


    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    gender = fields.Selection(string='Gender',
                            selection=[
                                        ('male', 'Male'),
                                        ('female', 'Female'),
                                        ('rather not say', 'Rather not say')
                                        ])
    nationality = fields.Many2one('res.country', string='Nationality')
    employment_status = fields.Char(string="Employment Status")
    employer_name = fields.Char(string='Employer Name')
    nature_of_job = fields.Char(string='Nature of Job')
    industry_segment = fields.Char(string="Industry Segment")
    interested_fields = fields.Char(string='Interested Fields')
    referral_name = fields.Char(string='Referral’s Name')
    company_address = fields.Text(string="Company Address")
    no_of_employees = fields.Selection([
                                        ('',''),
                                        ('1-4','1-4'),
                                        ('5-19','5-19'),
                                        ('20-49','20-49'),
                                        ('50-99','50-99'),
                                        ('100-499','100-499'),
                                        ('500-9999','500-9999')
                                        ])
    industry_sector = fields.Char('Type of Business')
    legal_representative = fields.Char('Legal Representative')
    designation = fields.Char('Designation')
    legal_number = fields.Char('Rep. Phone Number')
    contract_term = fields.Selection([
                                        ('',''),
                                        ('6 months','6 Months'),
                                        ('1 year','1 Year'),
                                        ('2 Year','2 Year'),
                                        ('>2 years','>2 Years')
                                    ])
    contract_from = fields.Date('Contract From')
    contract_to = fields.Date('Contract To')

    # send mail to created lead when click on submit in contact us page
    def action_send_crm_mail(self, email_from=None):
        template = False
        try:
            template = self.env.ref('customer_web_registration.mail_template_crm_lead')
        except ValueError:
            pass
        assert template._name == 'mail.template'        
        Mail = self.env['mail.mail']
        vals = {'auto_delete': False,
                'email_to': self.email_from,
                'subject': template.subject,
                'body_html': template.body_html,
                }       
        mail_id = Mail.sudo().create(vals)
        template.sudo().send_mail(self.id, force_send=True)
        
