# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

# from werkzeug.exceptions import NotFound
import werkzeug
import uuid

from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo import http, _ , fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class WebsiteSubscriptionSignature(CustomerPortal):

    @http.route(['/my/sale_subscription_custom/<int:subscription_id>/do_sign'], type='http', auth="user", website=True)
    def portal_sale_subscription_custom_do_sign(self, subscription_id, uuid=None, **kw):
        # account_res = request.env['sale.subscription']
        account_res = request.env['sale.order']

        if uuid:
            account = account_res.sudo().browse(subscription_id)
            if uuid != account.uuid:
                # raise NotFound()
                raise werkzeug.exceptions.NotFound()
        else:
            account = account_res.sudo().browse(subscription_id)
        if account.partner_id.id != request.env.user.partner_id.id:
            # raise NotFound()
            raise werkzeug.exceptions.NotFound()
        values = {
            'account': account,
        }
        return request.render("close_subscription_customer_sign.custom_subscription_sign", values)

    @http.route(['/my/sale_subscription_custom/<int:subscription_id>/accept_sign'], type='json', auth="user", website=True)
    def portal_my_sale_subscription_custom_signature(self, subscription_id, access_token=None, signature=None, download=False):
        try:
            # subscription = request.env['sale.subscription'].sudo().browse(subscription_id)
            subscription = request.env['sale.order'].sudo().browse(subscription_id)
        except (AccessError, MissingError):
            return {'error': _('Invalid subscription')}
        if not signature:
            return {'error': _('Signature is missing.')}
        else:
            subscription.write({
                'custom_signature_ids': [(0, 0 ,{
                    'signed_at': fields.Date.today(),
                    'signed_user_id': request.env.uid,
                    'custom_signature_img': signature,
                })],
                'custom_to_do_sign': False
            })

        return {
            'force_refresh': True,
            'redirect_url': '/my'
        }
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
