# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sh_show_terms_conditions_website_auth = fields.Boolean(
        related="website_id.sh_show_terms_conditions_website_auth", string="Show Terms & Conditions", readonly=False)
    sh_terms_title_auth = fields.Char(
        related="website_id.sh_terms_title_auth", string="Title", readonly=False, translate=True)
    sh_terms_label_auth = fields.Char(
        related="website_id.sh_terms_label_auth", string="Label", readonly=False, translate=True)
    sh_terms_text_auth = fields.Html(related="website_id.sh_terms_text_auth",
                                  string="Terms & Conditions", readonly=False, translate=True)
