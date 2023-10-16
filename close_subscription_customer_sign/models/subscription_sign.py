# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class SubscriptionSign(models.Model):
    _name = 'custom.subscription.signature'
    _description = 'Subscription Signature History'
    _rec_name = 'signed_user_id'

    signed_at = fields.Date(
        'Sign At',
        required=True,
    )
    signed_user_id = fields.Many2one(
        'res.users',
        'Signed by',
        required=True
    )
    custom_signature_img = fields.Binary(
        'Signature',
        copy=False,
        required=True
    )
    subscription_id = fields.Many2one(
        # 'sale.subscription',
        'sale.order',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
