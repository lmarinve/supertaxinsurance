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


class PolicyDetails(models.Model):
    _name = 'policy.details'

    name = fields.Char(string='Description', required=True)
    policy_number = fields.Integer(string="Policy Number", required=True,
                                   help="Policy number is a unique number that"
                                        "an insurance company uses to identify"
                                        "you as a policyholder")
    insurance_detail_id = fields.Many2one(
        'insurance.details', string='Insured ID', required=True)
    commission_rate = fields.Float(string='Commission %')
    start_date = fields.Date(
        string='Date Started', default=fields.Date.context_today, required=True)
    close_date = fields.Date(string='Date Closed', readonly=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    amount = fields.Monetary(string='Amount')
    invoice_ids = fields.One2many('account.move', 'insurance_id',
                                  string='Invoices', readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('closed', 'Closed')],
        required=True, default='draft')
    hide_inv_button = fields.Boolean(copy=False)

    policy_class_id = fields.Many2one(
        'policy.class', string='Policy Class', required=True)
    policy_group_id = fields.Many2one(
        'policy.group', string='Policy Group', required=True)
    policy_type_id = fields.Many2one(
        'policy.type', string='Policy Type', required=True)
    policy_carrier_id = fields.Many2one(
        'policy.carrier', string='Policy Carrier', required=True)
    payment_type = fields.Selection(
        [('fixed', 'Fixed'), ('installment', 'Installment')],
        required=True, default='fixed')
    policy_duration = fields.Integer(string='Duration in Days', required=True)
    note_field = fields.Html(string='Comment')

    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        if self.filtered(
                lambda reward: (
                        reward.commission_rate < 0 or reward.commission_rate > 100)):
            raise ValidationError(
                _('Commission Percentage should be between 1-100'))

    @api.constrains('policy_number')
    def _check_policy_number(self):
        if not self.policy_number:
            raise ValidationError(
                _('Please add the policy number'))

    def action_confirm_insurance(self):
        if self.amount > 0:
            self.state = 'confirmed'
            self.hide_inv_button = True
        else:
            raise UserError(_("Amount should be greater than zero"))

    def action_create_invoice(self):
        created_invoice = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.context_today(self),
            'partner_id': self.partner_id.id,
            'invoice_user_id': self.env.user.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': 'Invoice For Insurance',
                'quantity': 1,
                'price_unit': self.amount,
                'account_id': 41,
            })],
        })
        self.invoice_ids = created_invoice
        if self.policy_id.payment_type == 'fixed':
            self.hide_inv_button = False

    def action_close_insurance(self):
        for records in self.invoice_ids:
            if records.state == 'paid':
                raise UserError(_("All invoices must be paid"))
        self.state = 'closed'
        self.close_date = fields.Date.context_today(self)
        self.hide_inv_button = False



class PolicyClass(models.Model):
    _name = 'policy.class'

    name = fields.Char(string='Description')
    policy_group_ids = fields.One2many(
        'policy.group', 'policy_class_id', string='Policy Group')
    policy_carrier_ids = fields.One2many(
        'policy.carrier', 'policy_class_id', string='Policy Carrier')


class PolicyGroup(models.Model):
    _name = 'policy.group'

    name = fields.Char(string='Description')
    policy_class_id = fields.Many2one(
        'policy.class', string='Policy Class', required=True)
    policy_class_ids = fields.One2many(
        'policy.type', 'policy_group_id', string='Policy Type')


class PolicyType(models.Model):
    _name = 'policy.type'

    name = fields.Char(string='Description')
    policy_group_id = fields.Many2one(
        'policy.group', string='Policy Group', required=True)


class PolicyCarrier(models.Model):
    _name = 'policy.carrier'

    name = fields.Char(string='Description')
    policy_class_id = fields.Many2one(
        'policy.class', string='Policy Class', required=True)
