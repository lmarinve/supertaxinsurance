# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Odoo Advance Signup",
  "summary"              :  """Odoo admin can configure their signup page with dynamic fields for each website.""",
  "category"             :  "website",
  "version"              :  "1.1.0",
  "sequence"             :  10,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/",
  "description"          :  """
    advance signup in odoo
    signup page
    advance signup page
    odoo advance signup
    Enhanced signup page
    extra information signup
    odoo enhance signup
    password reset page
    reset login password
    odoo advance signup
    odoo advance signin
    odoo enhance login page
    odoo modified signup
    odoo signup custom fields
    odoo signup backgound image
    odoo signup terms and conditions
    odoo multi website signup
    odoo signup design
    odoo login page redesign

""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=advance_signup&custom_url=/web/login&lout=1",
  "depends"              :  [
                             'auth_signup',
                             'website',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'views/auth_signup_login_templates.xml',
                             'wizard/field_add_domain.xml',
                             'views/advance_signup_views.xml',
                             'views/res_partner_view.xml',
                             'data/adv_signup_data.xml',
                             'data/business_activity_data.xml',
                            ],
  "assets"               :  {
                            'web.assets_frontend':[
                              'advance_signup/static/src/css/adv_signup.css',
                              'advance_signup/static/src/js/adv_signup.js',
                            ]
  },
  "demo"                 :  [],
  "images"               :  ['static/description/Banner.gif'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  125,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
