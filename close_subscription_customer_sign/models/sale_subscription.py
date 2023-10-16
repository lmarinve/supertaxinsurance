# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class SaleSubscription(models.Model):
    # _inherit = 'sale.subscription'
    _inherit = 'sale.order'


    custom_to_do_sign = fields.Boolean(
        'To Do Sign',
        copy=False,
    )
    custom_signature_ids = fields.One2many(
        'custom.subscription.signature',
        'subscription_id',
        readonly=True,
    )

    def set_close(self):
        if self.is_subscription:
            template = self.env.ref("close_subscription_customer_sign.custom_email_template_subscription_colse_esign")
            template.send_mail(self.id)
            self.custom_to_do_sign = True
        return super(SaleSubscription, self).set_close()

    def _get_custom_subscription_signature_accept_url(self):
        self.ensure_one()
        return '/my/sale_subscription_custom/'+str(self.id)+'/accept_sign'

    def get_access_action(self):
        website_id = self.env['website'].search([('company_id','=',self.company_id.id)],limit=1)
        if website_id.domain:
            if website_id.domain.endswith('/'):
                domain_name = website_id.domain
                url = domain_name + '/my/sale_subscription_custom/' + str(self.id)+'/do_sign'
                return url
            else:
                domain = website_id.domain
                url = domain + '/my/sale_subscription_custom/' + str(self.id)+'/do_sign'
                return url
        else:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = base_url + '/my/sale_subscription_custom/' + str(self.id)+'/do_sign'
            return url      

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: