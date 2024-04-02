# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import http
from odoo.http import request, route
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class ContactUsLead(http.Controller):

    @http.route("/submitted/contact/lead", type="http", auth="public", website=True, csrf=True)
    # get value in lead page from contact us page.....
    def submit_contact_lead(self, **kw):
        vals = {
                "company_id": http.request.env.user.company_id.id,
                "email_from": kw.get("email_from"),
                "name": "Inquiry",
                "description" : kw.get('description'),
                "type": 'lead',
                "contact_name": kw.get("name"),
                "phone": kw.get("phone"),
                'partner_name': kw.get('company_name'),
                }
        lead_length = request.env["crm.lead"].sudo().create(vals)
        email_from = request.env.user.login
        # send mail to created lead when click on submit..
        lead_length.sudo().action_send_crm_mail(email_from)
        return request.render("customer_web_registration.contact_us_thankyou")


class AuthSignupRegistration(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public',website=True,sitemap=False)
    # redirect to company sign up form
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if qcontext:
            response_new = request.render('customer_web_registration.registration_page', qcontext)            
            return response_new

    @http.route('/web/signup/individual', type='http', auth='public',website=True,sitemap=False)
    # redirect to individual sign up form
    def web_auth_signup_individual(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if qcontext:
            response_new = request.render('customer_web_registration.individual_page', qcontext)            
            return response_new

    # get value in res.partner and res.user from individual sign up form submit
    @http.route("/submit/individual/user", type="http", auth="public", website=True, csrf=True)
    def submitted_individual_user(self, **kw):
        state_id = kw.get('state_id')
        country_id = kw.get('country_id')
        nationality = kw.get('nationality')
        vals = {
            "parent_id": kw.get('parent_id'),
            "login": kw.get("login"),
            "name": kw.get('first_name'),
            "first_name": kw.get('first_name'),
            "last_name": kw.get('last_name'),
            "birthdate": kw.get('Birthday'),
            "phone": kw.get('contact_number'),
            "gender": kw.get('gender'),
            "nationality": int(nationality) if nationality else False,
            "company_type": kw.get('company_type'),
            "employment_status": kw.get('employment_status'),
            "employer_name": kw.get('employer_name'),
            "nature_of_job": kw.get('nature_of_job'),
            "industry_segment": kw.get('industry_segment'),
            "interested_fields" : kw.get('interested_fields'),
            "referral_name": kw.get('referral_name'),
            "street": kw.get("Street"),
            "state_id": int(state_id) if state_id else False,
            "country_id": int(country_id) if country_id else False,
            'email': kw.get('login'),
            'comment': kw.get('description'),
        }
        request.env["res.users"].sudo().create(vals)
        return request.render("customer_web_registration.registration_thankyou")

    # get value in res.partner and res.user from company sign up form submit
    @http.route("/submit/company/user", type="http", auth="public", website=True, csrf=True)
    def submitted_company_user(self, **kw):
        vals = {
            "parent_id": kw.get('parent_id'),
            "login": kw.get("login"),
            'email': kw.get('login'),
            'phone': kw.get('contact_number'),
            "name": kw.get("company_name"),
            'company_name': kw.get('company_name'),
            'street': kw.get('street'),
            'country_id': int(kw.get('country_id')),
            'company_type': kw.get('company_type'),
            'no_of_employees': kw.get('no_of_employees'),
            'industry_sector': kw.get('industry_sector'),
            'legal_representative': kw.get('legal_representative'),
            'designation': kw.get('designation'),
            'legal_number': kw.get('legal_number'),
            'contract_term': kw.get('contract_term'),
            'contact_number': kw.get("contact_number"),
            'contract_from': kw.get('contract_from') or str(datetime.datetime.now().date()),
            'contract_to': kw.get('contract_to') or str(datetime.datetime.now().date()),
            'comment': kw.get('description'),        
            }
        request.env["res.users"].sudo().create(vals)
        return request.render("customer_web_registration.registration_thankyou")
