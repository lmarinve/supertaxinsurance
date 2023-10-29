# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    sh_show_terms_conditions_website_auth = fields.Boolean(
        "Show Terms & Conditions?")
    sh_terms_title_auth = fields.Char("Title", translate=True)
    sh_terms_label_auth = fields.Char("Label", translate=True)
    sh_terms_text_auth = fields.Html("Terms & Conditions", translate=True)
