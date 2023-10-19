# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sign Up Terms & Conditions",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "category": "Website",
    "summary": """
show signup terms & condition,
create signup terms-condition,
signup terms and condition,signup tnc
sign up tnc sign up terms
term and condition module odoo
""",
    "description": """
This module is used to display terms and conditions
when any user is signing up on your website.
If you want to add terms and condition boolean at the bottom
of the signup form. Easy to create signup
terms and conditions using this module and set into the website sign up form.
To create terms and conditions install this module
and go to the website configuration setting
then check the right "Show Terms and Conditions".
""",
    "depends": ["website", "auth_signup"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/sh_signup_tnc_auth_templates.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_signup_tnc/static/src/js/sh_signup_tnc.js',
        ],
    },
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": 15,
    "currency": "EUR"
}
