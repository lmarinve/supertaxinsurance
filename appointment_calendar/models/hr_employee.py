# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    calendar_id = fields.Many2one('appointment.calendar', string='Booking Calendar')
    is_available = fields.Boolean(string='Is for Appointment')
