# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': "Supertax Insurance Web Registration",
    'version': '16.0.1.0',
    'license': 'OPL-1',
    'summary': """Customer Registration Form | customer registration form |
                  Customer Registration Process | customer registration process |
                  Customer Registration | customer registration""",
    'category': 'Web',
    'description': """Supertax Insurance Registration Process""",
    'author': 'Supertax Insurance',
    'website': 'https://www.supertaxinsurance.com',
    'depends': [
                'base', 
                'website',
                'website_slides', 
                'website_crm', 
                'crm',
                'hr',
                ],
    'data': [
            'data/contact_us_mail.xml',
            'views/contact_us_form.xml',
            'views/contact_us_thankyou.xml',
            'views/crm_lead_view.xml',
            'views/hr_employee_view.xml',
            'views/reg_company.xml',
            'views/reg_individual.xml',
            'views/reg_thankyou.xml',
            'views/res_partner_view.xml',
            'views/website_view.xml',
            ],
    'assets':{
            'web.assets_frontend': [
                'customer_web_registration/static/src/js/reg_hide_fields.js',
            ],
    },
    'images': ['static/description/banner.jpg'],
    'price': 21.00,
    'currency': 'EUR',
}
