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
    no_of_employees = fields.Selection([
                                        ('', ''), 
                                        ('>20', '>20'), 
                                        ('20-50', '20-50'), 
                                        ('50-70', '50-70'), 
                                        ('70-100', '700-100')
                                        ])
    no_registered_employee = fields.Integer(string="Registered Employee")
    industry_sector = fields.Char(string="Industry Sector")
    course_id = fields.Many2one('slide.channel', string='Select Course')
    contract_term = fields.Selection([
                                    ('', ''), 
                                    ('6 months', '6 Months'), 
                                    ('1 year', '1 Year'), 
                                    ('2 years', '2 Years'), 
                                    ('>2 years', '>2 Years')
                                    ])
    designation = fields.Char(string="Designation")
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
        