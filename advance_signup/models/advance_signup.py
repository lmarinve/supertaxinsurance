# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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

from odoo import models, fields, api, _
from odoo.exceptions import UserError

SIGNUP_FIELD_TYPES = [
    'char',
    'integer',
    'float',
    'boolean',
    'text',
    'selection',
    'many2one',
    'many2many',
    'binary',
    'date'
]
FIELDS_INPUT_TYPE = [
    ('char', 'text'),
    ('integer', 'number'),
    ('float', 'float'),
    ('boolean', 'checkbox'),
    ('text', 'textarea'),
    ('selection', 'selection'),
    ('many2one', 'selection_m2o'),
    ('many2many', 'selection_m2m'),
    ('binary','binary'),
    ('date','date')
]

class AdvSignupSettings(models.Model):
    _name = "adv.signup.settings"
    _order = "active desc"
    _description = "Advance Signup Fields"

    def write(self,vals):
        if vals.get('website_id',False):
            vals.update({'active':False})
        return super().write(vals)


    @api.model
    def get_active_website_setting(self, website_id):
        active_rec = self.search([('website_id','=',int(website_id)),('active','=',True)], limit=1)
        if active_rec:
            return active_rec
        return False

    def _default_website(self):
        return self.env['website'].search([
            ('company_id', '=', self.env.user.company_id.id)],
            limit=1,
        )

    website_id = fields.Many2one('website',
        string= "Website",
        default= _default_website,
        ondelete= 'cascade',
        required= True,
        )
    name= fields.Char("Name", required=True, translate=True)
    active = fields.Boolean('Active', default=False, copy=False)
    hide_header = fields.Boolean("Hide header from Signup Page",
        copy= True,
        )
    hide_footer = fields.Boolean("Hide footer from Signup Page",
        copy= True,
        )
    show_t_n_c = fields.Boolean("Show Terms and Condition in Signup Page",
        copy= True,
        )
    background_type = fields.Selection([
        # ('color','Color'),
        ('image','Image'),
        ('none','None'),
        ], string= "Background Type",
        default= "none",
        copy= True,
        readonly= False,
        )
    bg_img = fields.Binary("Background Image",
        copy=True,
        readonly=False,
        )
    signup_page_content = fields.Html("SignUp Page Content",
        copy=True,
        translate=True,
        readonly=False,
        default='<p><span style="color: rgb(160, 160, 160); font-family: Georgia,\
         Times, &quot;Times New Roman&quot;, serif; font-style: italic; \
         font-variant-ligatures: initial; font-variant-caps: initial; font-weight: initial;\
         text-align: inherit;">Please enter the information to create your account</span></p>'
        )
    login_page_content = fields.Html("Login Page Content",
        copy=True,
        translate=True,
        readonly=False,
        default='<p><span style="color: rgb(160, 160, 160); font-family: Georgia,\
         Times, &quot;Times New Roman&quot;, serif; font-style: italic;">Please Log In</span></p>'
        )
    reset_passw_page_content = fields.Html("Reset Password Content",
        copy=True,
        translate=True,
        readonly=False,
        default='<p><span style="color: rgb(160, 160, 160); font-family: Georgia,\
         Times, &quot;Times New Roman&quot;, serif; font-style: italic;">Please \
         enter your email. You will receive a reset password link</span></p>'
        )
    t_n_c_content = fields.Html("Terms and Condition",
        copy=True,
        translate=True,
        default="<p> Terms and Condition <p>"
        )
    signup_field_ids = fields.One2many("adv.signup.fields",
        "adv_signup_setting_id",
        "SignUp Fields",
        )

    @api.constrains('signup_field_ids')
    def _check_signup_field_ids(self):
        if not self.signup_field_ids:
            raise UserError(_('Atleast one record should be there for signup fields.'))

    def toggle_active(self):
        active_website_setting = self.search(
            [('active', '=', True),('website_id', 'in', [self.website_id.id])], limit=1)
        if active_website_setting and not self.active:
            active_website_setting.active = False
            self.active = True
        else:
            self.active = not self.active
        return

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("website_id"):
                active_website_setting = self.search(
                    [('active', '=', True),('website_id', 'in', [int(vals.get("website_id"))])])
                if not active_website_setting:
                    vals.update({'active':True,})
            res = super(AdvSignupSettings, self).create(vals)
        return res

class AdvSignupFields(models.Model):
    _name = "adv.signup.fields"
    _order = "sequence"
    _description = "Advance Signup Fields"

    @api.depends("field_type")
    def _compute_field_input_type(self):
        for rec in self:
            field_type = rec.field_type
            if field_type:
                input_type = [item for item in FIELDS_INPUT_TYPE if field_type in item[0]]
                if input_type and input_type[0] and input_type[0][1]:
                    rec.field_input_type = input_type[0][1]

    field = fields.Many2one("ir.model.fields", "Signup Field",
        required=True, help="Associated field in the SignUp form.",
        domain="[('model', 'in', ['res.partner']),('ttype', 'in', %s),('name','not in',['email','name'])]" % SIGNUP_FIELD_TYPES,
        ondelete='cascade',
    )
    field_type = fields.Selection(
            related = "field.ttype",
            store = True,
            readonly = True,
            string = "Field Type",
            help="Associated field type in the SignUp form.",)
    field_domain = fields.Char("Field Domain")
    field_input_type = fields.Char("Input Type", help="Field input type in signup form",
        compute = "_compute_field_input_type", store=True)
    no_of_cols = fields.Selection([('1','1'),('2','2')], "Number of columns",
        help="Number of columns in signup form")
    is_required = fields.Boolean("Is required",
        help="Enable if associated field will be required")
    sequence = fields.Integer("Sequence",
        help="Sequence number for this field in signup form")
    field_label = fields.Char("Field Label",
        help="Label for this field in signup form",
        translate=True)
    placeholder = fields.Char("Placeholder",
        help="Placeholder value for this field in signup form",
        translate=True)
    help = fields.Text("Help",
        help="Description for this field to customers in signup form",
        translate=True)
    adv_signup_setting_id = fields.Many2one("adv.signup.settings", "Signup Settings")
    file_type = fields.Text("File type")
    file_max_size = fields.Float("File max size",default="500.00",help="Allowed size depends on odoo server which is allowed to upload.")

    @api.onchange("field")
    def _compute_field_label(self):
        for rec in self:
            if rec.field:
                rec.field_label = rec.field.field_description
                rec.field_domain = ''

    def get_field_obj_relation(self):
        for rec in self:
            obj_relation = None
            field = rec.field
            if field and rec.field_type in ['many2one', 'many2many']:
                obj_relation = field.relation
        return obj_relation

    def action_add_domain(self):
        obj_relation = self.get_field_obj_relation()
        view_id = self.env["field.add.domain"].create({})
        vals = {
            'name' : _("Add Domain"),
            'view_mode' : 'form',
            # 'view_type' : 'form',
            'res_model' : 'field.add.domain',
            'res_id' : view_id.id,
            'context' : "{'obj_relation': '%s'}" % obj_relation,
            'type' : "ir.actions.act_window",
            'target' : 'new',
         }
        return vals
