# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import datetime
import werkzeug.urls
import urllib
from urllib.request import urlretrieve
from urllib.parse import urlparse
from odoo import http, SUPERUSER_ID, tools, _
from odoo import api, fields, models, _
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import ensure_db
from odoo.exceptions import UserError, ValidationError
from odoo.tools import pycompat

import logging
_logger = logging.getLogger(__name__)

class AuthSignupHome(Home):

    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        response = super(AuthSignupHome, self).web_login(*args, **kw)
        if kw:
            if ('login' not in kw):
                if 'token' not in kw:
                    if 'redirect' in kw:
                        del kw['redirect']
                    x = urllib.parse.urlencode(kw)
                    key_arg = urllib.parse.unquote(x)
                    response.qcontext.update(self.get_auth_signup_config())
                    a = b = c = ''
                    if key_arg != '':
                        if '&' in key_arg:
                            a, b = key_arg.split('&',1)
                    b = b[:-1]
                    partner = None
                    if a != '' and b != '':
                        key1 , value1 = a.split('=',1)
                        key2 , value2 = b.split('=',1)
                        dic1 = dict(key1=value1,key2=value2)  
                        partner_obj = request.env['res.partner']
                        if (dic1['key1']).isdigit():
                            partner = int(dic1['key1'])
                        elif (dic1['key2']).isdigit():
                            partner = int(dic1['key2'])
                        elif request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
                            # Redirect if already logged in and redirect param is present
                            return http.redirect_with_hash(request.params.get('redirect'))
                        else:
                            return response
                        if partner != None:
                            partner_id = partner_obj.sudo().search([('id','=',partner)])

                        partner_id.sudo().signup_prepare()
                        redirect_url = partner_id.signup_url
                        if redirect_url:
                            return request.redirect(redirect_url)
                else:
                    if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
                        # Redirect if already logged in and redirect param is present
                        return http.redirect_with_hash(request.params.get('redirect'))

        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get('redirect'))
        return response

class WebsitePoralUserInvitation(http.Controller):

    @http.route(['/my/invitation/request'], type='http', auth="public", website=True)
    def invitation_request(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        _logger.info("******** my/invitation/request ********")
        _logger.info(f"cr: {cr}")
        _logger.info("******** uid ********")
        _logger.info(f"uid: {uid}")
        _logger.info("******** context ********")
        _logger.info(f"context: {context}")
        _logger.info("******** pool ********")
        _logger.info(f"pool: {pool}")
        _logger.info("****************")


        return request.render("website_portal_user_join_invitation.invitation_request")

    @http.route(['/my/invitation/request/confirm/'], type='http', auth="public", website=True)
    def invitation_confirm(self, **post):
        if post.get('debug'):
            return request.render("website_portal_user_join_invitation.invitation_thankyou")
        if not post:
            return request.render("website_portal_user_join_invitation.invitation_thankyou")
        user_id = post['user_id']
        name = post['name']
        email = post['email']

        invitation_obj = request.env['res.users.invitation']
        partner_obj = request.env['res.partner']
        invitation_create = invitation_obj.sudo().search([('email','=',email)])
        user_ids = False
        if invitation_create.id:
            user_ids = request.env['res.users'].search([('email','=',email)],limit=1)
        if not invitation_create.id: 
            invitation_create = invitation_obj.create({ 'name': name, 'email': email, 'invitation_date': datetime.datetime.now(), 'user_id': int(user_id),'website_port_sample':http.request.httprequest.host_url })
        if user_ids:
            partner_id = partner_obj.sudo().search([('email','=',email),('user_ids','=',user_ids.id)])
        else:
            partner_id = partner_obj.sudo().search([('email','=',email)])
        if not partner_id.id:
            partner_id = partner_obj.sudo().create({
                'name':name,
                'email':email,
            })

        lang = request.env.user.lang
        company_id = request.env.user.company_id.id
        user = request.env['res.users'].sudo().search([('login','=',email)])
        if user:
            return request.redirect("/my/invitation/request?already_user=1")
        else:
            new_user = request.env['res.users'].sudo().with_context(no_reset_password=True)._create_user_from_template({
                'email': email,
                'login': email,
                'partner_id': partner_id.id,
                'company_id': company_id,
                'company_ids': [(6, 0, [company_id])],
            })
        
        base_url = partner_id.sudo().get_base_url()
        route = 'login'
        query = dict(db=request.env.cr.dbname,partner=partner_id.id)

        final_url = werkzeug.urls.url_join(base_url, "/web/%s?%s" % (route,werkzeug.urls.url_encode(query)))


        if request.session.uid:
            su_id = request.env['res.users'].sudo().browse(request.env.user.id)
            template_id = request.env['ir.model.data']._xmlid_to_res_id('website_portal_user_join_invitation.email_template_join_user_invitation')
            email_template_obj = request.env['mail.template'].sudo().browse(template_id)
            if template_id:
                values = email_template_obj.generate_email(invitation_create.id, fields=['email_from'])
                values['email_from'] = su_id.email
                values['email_to'] = email
                values['subject'] = 'Invitation Mail to Join' + request.env.user.company_id.name
                values['author_id'] = request.env['res.users'].browse(request.env.uid).partner_id.id
                values['body_html'] = """
                    <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">
                        <p><strong>Dear %s !!! </strong></p>
                        <p><strong>%s has Invited to Join %s! </strong></p>
                    </div>
                     <br/>
                        <a href=%s class="btn btn-default mb32" style="background-color:#337ab7;color:#fff;text-decoration:inherit;-webkit-user-select:none;border-bottom-left-radius:0px;border-bottom-right-radius:0px;border-top-right-radius:0px;border-top-left-radius:0px;line-height:1.42857;font-size:13px;padding-left:12px;padding-bottom:6px;padding-right:12px;padding-top:6px;white-space:nowrap;border-image-repeat:initial;border-image-outset:initial;border-image-width:initial;border-image-slice:initial;border-image-source:initial;border-left-color:initial;border-bottom-color:initial;border-right-color:initial;border-top-color:initial;border-left-style:none;border-bottom-style:none;border-right-style:none;border-top-style:none;border-left-width:initial;border-bottom-width:initial;border-right-width:initial;border-top-width:initial;background-image:none;cursor:pointer;touch-action:manipulation;vertical-align:middle;text-align:center;font-weight:normal;margin-bottom:0px;display:inline-block;">Accept</a>
                    """ % (str(name),str(request.env.user.name),str(request.env.user.company_id.name),final_url)
                mail_mail_obj = request.env['mail.mail']
                msg_id = mail_mail_obj.sudo().create(values)
                if msg_id:
                    sends = mail_mail_obj.sudo().send([msg_id])
                    msg_id.sudo().send()

        else:   
            su_id = request.env['res.users'].sudo().browse(int(user_id))
            template_id = request.env['ir.model.data']._xmlid_to_res_id('website_portal_user_join_invitation.email_template_join_request_invitation')
            email_template_obj = request.env['mail.template'].browse(template_id)
            if template_id:
                values = email_template_obj.sudo().generate_email(invitation_create.id, fields=['email_from'])
                values['email_from'] = email
                values['email_to'] = su_id.email
                values['subject'] = 'Join Invitation Mail' + request.env.user.company_id.name
                values['author_id'] = su_id.partner_id.id
                values['body_html'] = """
                    <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">
                        <p><strong>Dear %s !!! </strong></p>
                        <p><strong>%s wants to Join %s! </strong></p>
                        <p><strong>Details: </strong></p>
                        <p><strong>NAME:</strong> %s </p>
                        <p><strong>EMAIL:</strong> %s </p>
                    </div>
                    """ % (su_id.name, str(name), str(request.env.user.company_id.name), str(name), str(email))
                mail_mail_obj = request.env['mail.mail']
                msg_id = mail_mail_obj.sudo().create(values)
                if msg_id:
                    sends = mail_mail_obj.sudo().send([msg_id])
                    
                                                    
        return request.render("website_portal_user_join_invitation.invitation_thankyou")
           
    @http.route(['/welcome'], type='http', auth="none", methods=['GET'])
    def user_welcome(self, **post):

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        values ={}
        values.update({
                    'countries': countries,
                    'states': states,
            })
        return request.render("website_portal_user_join_invitation.invited_user",values)

    @http.route(['/process/request/'], type='http', auth="public", website=True)
    def process_user_request(self, **post):
        if post['pswd'] == post['pswd2']:
            match = request.env['res.users'].sudo().search([('login','=',post['email'])])
            if match:
                return request.redirect("/welcome?email_exists=1")
            else:

                user_obj = request.env['res.users']
                user = user_obj.sudo().create({ 
                    'name' : post['name'],
                    'login' : post['email'],
                    'password' : post['pswd'],
                })
                return request.render("website_portal_user_join_invitation.user_thankyou")
        else:
            return request.redirect("/welcome?wrong_pswd=1")




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
