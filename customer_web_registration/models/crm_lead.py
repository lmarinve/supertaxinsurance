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
                                        ('1-4','1-4'),
                                        ('5-19','5-19'),
                                        ('20-49','20-49'),
                                        ('50-99','50-99'),
                                        ('100-499','100-499'),
                                        ('500-9999','500-9999')
                                        ])
    family_members = fields.Integer(string="Family Members")
    industry_sector = fields.Char(string="Industry Sector")
    carrier_id = fields.Many2one('slide.channel', string='Select Carrier')
    contract_term = fields.Selection([
                                    ('', ''),
                                    ('1 time','1 time'),
                                    ('1 year','1 Year'),
                                    ('>1 years','>1 Years')
                                    ])
    estimated_premium = fields.Integer(string="Estimated Premium")
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
        
