# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo Sign Up Invitation Emails(MLM)',
    'summary':'App Send Invitation to Portal User to Join Website Invite contacts portal invite Customer Portal email Inviting customer User invitation email website Portal Invitation website shop Invitation sign up portal Join Portal Invitation website MLM for website',
    'category': 'eCommerce',
    'version': '16.0.0.0',
    'author': 'BrowseInfo',
    "website" : "https://www.browseinfo.com",
    'description': """
       webstore send invitation emails webstore
""",
    'depends': ['website'],
    "price": 19,
    "currency": "EUR",
    'data': [
        'security/ir.model.access.csv',
        #'data/data.xml',
        'views/res_users_view.xml',
        'edi/user_invitation_email.xml',
        'views/templates.xml',
    ],
    'license':'OPL-1',
    'application': True,
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/owlKAt760n0',
    "images":["static/description/Banner.gif"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
