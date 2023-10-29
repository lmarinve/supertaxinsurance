# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InsuranceDetails(models.Model):
    _name = 'insurance.details'

    name = fields.Char(
        string='Name', required=True, copy=False, readonly=True, index=True,
        default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True)
    policy_ids = fields.One2many(
        'policy.details', 'insurance_detail_id', string='Policy')
    employee_id = fields.Many2one(
        'employee.details', string='Agent', required=True)
    note_field = fields.Html(string='Comment')


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'insurance.details') or 'New'
        return super(InsuranceDetails, self).create(vals)
