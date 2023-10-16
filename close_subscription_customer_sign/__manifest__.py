# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Customer Signature on Close Subscription ',
    'version' : '3.2.3',
    'category': 'Sales/Subscriptions',
    'depends' : [
        'website',
        'sale_subscription',
     ],
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'images': ['static/description/img1.jpg'],
    'price': 9.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': 'Close Subscription with Customer Signature',
    'website': 'www.probuse.com',
    # 'live_test_url' : 'https://probuseappdemo.com/probuse_apps/close_subscription_customer_sign/271',#'https://youtu.be/liS10jG4ovM',
    'description': ''' 
Close Subscription Customer Signature.
To do Signature from email button link
 ''',
    'data' : [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/template.xml',
        'views/subscription_view.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
