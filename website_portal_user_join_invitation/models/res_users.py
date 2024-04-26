# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
	_inherit = 'res.users'

	invitation_ids = fields.One2many('res.users.invitation', 'user_id', string='Invitations')
	
	
class ResUsersInvitation(models.Model):
	_name = "res.users.invitation"
	_description = "List of Users Invitation"

	user_id = fields.Many2one('res.users', string='Referral User')
	name = fields.Char(string='Invited Username')
	email = fields.Char(string='Invited User Email')
	invitation_date = fields.Datetime(string='Invitation Date')
	website_port_sample = fields.Char('Website')


class Website(models.Model):
	_inherit = 'website'

	def get_users_list(self):            
		user_ids=self.env['res.users'].sudo().search([('share', '=', False)])
		return user_ids
				
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
