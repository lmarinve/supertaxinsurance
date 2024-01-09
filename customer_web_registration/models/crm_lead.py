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

    company_address = fields.Text(string="Company Address")
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
    industry_sector = fields.Char('Industry Sector')
    industry_segment = fields.Char(string="Industry Segment")
    no_of_employees = fields.Selection([
                                        ('', ''),
                                        ('1-4', '1-4'),
                                        ('5-19', '5-19'),
                                        ('20-49', '20-49'),
                                        ('50-99', '50-99'),
                                        ('100-499', '100-499'),
                                        ('500-9999', '500-9999')
                                        ])
    interested_products = fields.Char(string='Interested Products')
    referral_name = fields.Char(string='Referral’s Name')
    birthday = fields.Date(string='Birthday')

    contact_number = fields.Char(string="Contact Number")

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
        
