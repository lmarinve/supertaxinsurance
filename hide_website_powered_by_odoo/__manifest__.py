# -*- coding: utf-8 -*-
{
    'name': 'Hide Powered By Odoo Footer',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'summary': """
        Hide The Phrase Powered By Odoo located in the Website Footer.
    """,
    'description': "Hide The Powered By Odoo in the website Footer.",
    'author': 'Emad Al-Futahi',
    'maintainer': 'Emad Al-Futahi',
    'price': '5.0',
    'currency': 'USD',
    'license': 'OPL-1',
    'support':'eakram26@gmail.com',
    'depends': ['website']
    ,
    'data': [
        'views/webclient_templates.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
