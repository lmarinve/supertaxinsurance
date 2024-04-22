# -*- coding: utf-8 -*-
#############################################################################
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
#############################################################################

from odoo import api, fields, models, _
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

class Website(models.Model):
    _inherit = 'website'

    def get_active_website_setting(self):
        website_id = self.env['website'].get_current_website()
        if website_id:
            website_id.clear_caches()
            active_rec = self.env['adv.signup.settings'].sudo().search([('website_id','=', website_id.id),('active','=',True)], limit=1)
            return active_rec
        return False

    def get_all_field_values(self, field_id):
        f_values = {}
        field = self.env['adv.signup.fields'].browse(int(field_id))
        domain = field.field_domain or []
        obj_rel = field.sudo().get_field_obj_relation()
        if domain:
            domain = safe_eval(domain)
        objs = self.env[obj_rel].sudo().search(domain)
        if objs:
            for rec in objs:
                field_type = field.sudo().field
                if field_type.name.startswith('property_'):
                    f_values[field_type.relation + ',' + str(rec.id)] = rec.name
                else:
                    f_values[rec.id] = rec.name if 'name' in rec._fields else rec.name_get()[0][1]
        return f_values

    def get_signup_fields(self):
        signup_obj = self.get_active_website_setting()
        signup_field_list = []
        if signup_obj:
            if signup_obj.signup_field_ids:
                for field in signup_obj.signup_field_ids:
                    field_dict = {}
                    f_name = field.field.name
                    f_input_type = field.field_input_type
                    field_dict[f_name] = {
                        'input_type': field.field_input_type,
                        'placeholder': field.placeholder or '',
                        'title': field.help or '',
                        'label': field.field_label or field.field.field_description or '',
                        'is_required': field.is_required,
                        'cols': int(field.no_of_cols),

                    }
                    if f_input_type == 'binary':
                        field_dict[f_name].update({
                        'supported_file_type':field.file_type,
                        'max_size':field.file_max_size})
                    if f_input_type == 'selection':
                        if request.env['res.partner'].fields_get().get(f_name):
                            f_values = dict(request.env['res.partner'].fields_get()[f_name]['selection'])
                            field_dict[f_name].update({'f_values': f_values})
                    if f_input_type in ['selection_m2o', 'selection_m2m']:
                        f_values = self.get_all_field_values(field.id)
                        field_dict[f_name].update({'f_values': f_values})
                    signup_field_list.append(field_dict)
        return signup_field_list

    def is_login_signup_page(self):
        path = request.httprequest.full_path
        if path.find("/web/login") == 0 or path.find("/web/signup") == 0 or path.find("/web/reset_password") == 0:
            return True
        return False

    def is_signup_page(self):
        self.clear_caches()
        if request.httprequest.full_path.find('/web/signup') == 0:
            return True
        return False
