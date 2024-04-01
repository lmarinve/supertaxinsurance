# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, api, http
from odoo.addons.base.models.ir_mail_server import MailDeliveryException


# inherit res.users and add new fields(not in view) for sign up form to create portal user...
class ResUserInherit(models.Model):
    _inherit = 'res.users'
    
    @api.model_create_multi
    def create(self, vals_list):
        # create user from sign up form
        self.env.cr.execute("""SELECT id FROM res_users order by id asc""")
        active_channels = self.env.cr.dictfetchall()
        multi_id = active_channels[-1].get('id')
        res_object = self.env['res.users'].search([('id','=', multi_id)])
        result = super(ResUserInherit, self).create(vals_list)
        result.write({'groups_id': [(3, self.env.ref('base.group_user').id),(4, self.env.ref('base.group_portal').id)]})

        if result.company_type == 'person':
            resultant_parent_id = None
            indiviual_vals = {
                                'name': result.name,
                                'company_type': result.company_type,
                                'employment_status': result.employment_status,
                                'nature_of_job': result.nature_of_job,
                                'referral_name': result.referral_name,
                                'birthdate': result.birthdate,
                                'gender': result.gender,
                                'country_id': result.country_id.id,
                                }
            result.partner_id.write(indiviual_vals)
            if result.id:
                indiviual_vals.update({'user_id': result.id})
            if result.partner_id:
                result.partner_id.email = result.login
                if result.parent_id:
                    result.partner_id.parent_id = result.parent_id.id
            result.employee_id.create(indiviual_vals)
            if result.employee_id:
                result.employee_id.update({
                                            'work_email': result.login,
                                            'birthday': result.birthdate,
                                            'phone': result.contact_number,
                                            'country_of_birth': result.country_id.id,
                                            })
            if not self.env.context.get('no_reset_password'):
                users_with_email = result.filtered('email')
                if users_with_email:
                    try:
                        users_with_email.with_context(create_user= True).action_reset_password()
                    except MailDeliveryException:
                        users_with_email.partner_id.with_context(create_user= True).signup_cancel()
            
        if result.company_type == 'company':
            # create inactive portal user from sign up company form.
            result.active = False
            company_vals = {
                            'name': result.company_name,
                            'company_type': result.company_type,
                            'company_name': result.name,
                            'no_of_employees': result.no_of_employees,
                            'industry_sector': result.industry_sector,
                            'family_members': result.family_members,
                            'contract_term': result.contract_term,
                            'susbcription_fee': result.susbcription_fee,
                            'prior_agreed_fees': result.prior_agreed_fees,
                            'start_contract_date': result.start_contract_date,
                            'expiry_contrat_date': result.expiry_contrat_date,
                            'estimated_premium': result.estimated_premium,
                            }
            if result.partner_id:
                result.partner_id.email = result.login
                result.partner_id.write(company_vals)
            if result.id:
                company_vals.update({   
                                        'user_id': result.id, 
                                        'work_email': result.login,
                                        'phone': result.contact_number,
                                    })
            result.employee_id.create(company_vals)

        return result
        
