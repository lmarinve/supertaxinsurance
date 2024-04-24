# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from datetime import datetime, timedelta

from odoo import fields, http
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class MemberAppointment(http.Controller):

    @http.route('/appointment/member', auth="public", website=True)
    def team_list(self, **post):
        employees = request.env['hr.employee'].sudo().search([('is_available', '=', True)])
        return request.render('appointment_calendar.appointment_select_employee', {'employees': employees})

    @http.route('/appointment/member/<int:employee_id>/<int:calendar_id>', auth="public", website=True)
    def calendar(self, employee_id=None, day=None, calendar_id=None, selectedDate=None, **post):
        calendar = request.env['appointment.calendar'].sudo().browse(int(calendar_id))
        cal_lines = request.env['appointment.calendar.line'].sudo().search([('line_id', '=', calendar.id)])
        today = datetime.now()
        today.strftime("%B")
        month_year = '%s  %s' % (today.strftime("%B"), today.year)
        minutes_slot = calendar.minutes_slot
        days = []
        for c in cal_lines:
            s_date = c.start_datetime
            if s_date.day not in days:
                days.append(s_date.day)
        values = {
            'cal_lines': cal_lines,
            'days': days,
            'calendar_id': calendar.id,
            'employee_id': employee_id,
            'month_year': month_year,
            'minutes_slot': minutes_slot
        }
        return request.render('appointment_calendar.appointment_member_calendar', values)

    @http.route('/appointment/book', auth="public", website=True)
    def book_time(self, **post):
        if post.get('selectedDate') and post.get('selectedTime'):
            date_time = '%s %s' % (post.get('selectedDate'), post.get('selectedTime'))
            start_date = datetime.strptime(date_time, '%d-%m-%Y %H:%M')
            minutes_slot = post.get('minutes_slot')
            employee = request.env['hr.employee'].sudo().browse(int(post.get('employee_id')))
            calendar_id = post.get('calendar_id')
            stop_date = start_date + timedelta(minutes=int(minutes_slot))
            values = ({
                'booking_time': '%s | %s %s , %s' % (post.get('selectedTime'), start_date.strftime('%B'), start_date.day, start_date.year),
                'start_datetime': fields.Datetime.to_string(start_date),
                'start': fields.Datetime.to_string(start_date),
                'stop': fields.Datetime.to_string(stop_date),
                'duration': round((float(minutes_slot) / 60.0), 2),
                'calendar_id': int(calendar_id),
                'minutes_slot': int(post.get('minutes_slot')),
                'employee': employee
            })
            return request.render('appointment_calendar.appointment_book', values)

    @http.route('/appointment/book/confirm', auth="public", website=True)
    def confirm_booking(self, **post):
        Employee = request.env['hr.employee'].sudo()
        employee = Employee.search([('work_email', '=', post.get('work_email'))], limit=1)
        if post.get('calendar_id'):
            calendar_id = request.env['appointment.calendar'].sudo().browse(int(post.get('calendar_id')))
            start_date = datetime.strptime(post.get('start_datetime'), '%Y-%m-%d %H:%M:%S')
            utc_date = calendar_id.get_utc_date(start_date, calendar_id.tz)
            stop_date = utc_date + timedelta(minutes=int(post.get('minutes_slot')))
            team_member = Employee.browse(int(post.get('employee_id')))
            post['team_member'] = team_member
            if not employee:
                employee = Employee.create({
                    'name': "%s %s" % (post.get('first_name'), post.get('last_name') and post.get('last_name') or ''),
                    'work_email': post.get('work_email'),
                    'work_phone': post.get('work_phone'),
                    'tz': post.get('timezone'),
                })
            event = {
                'name': '%s-%s' % (post.get('first_name'), post.get('start_datetime')),
                'employee_ids': [(6, 0, [employee.id, int(post.get('employee_id'))])],
                # 'start_datetime': fields.Datetime.to_string(utc_date),
                'duration': float(post.get('duration')),
                'start': fields.Datetime.to_string(utc_date),
                'stop': fields.Datetime.to_string(stop_date),
                'alarm_ids': [(6, 0, calendar_id.alarm_ids.ids)],
            }
            app = request.env['calendar.event'].sudo().with_context({'no_mail': True}).with_user(2).create(event)
            app.attendee_ids.write({'state': 'accepted'})
            domain = [('line_id', '=', int(post.get('calendar_id'))), ('start_datetime', '=', fields.Datetime.to_string(utc_date)), ('end_datetime', '=', fields.Datetime.to_string(stop_date))]
            lines = request.env['appointment.calendar.line'].sudo().search(domain)
            for line in lines:
                if line.start_datetime == fields.Datetime.to_string(utc_date) and line.end_datetime == fields.Datetime.to_string(stop_date):
                    line.unlink()
            post['event_id'] = app
            # mail_ids = []
            # Mail = request.env['mail.mail'].sudo()
            # template = request.env.ref('kanak_appointment_advanced.kanak_calendar_booking')
            # for attendee in app.attendee_ids:
            #     Mail.browse(template.sudo().send_mail(attendee.id)).send()
            # post['date'] = date_appointment
            return request.render('appointment_calendar.appointment_thankyou', post)

    @http.route('/calendar/timeslot', type='json', auth='public')
    def get_time_slots(self, calendar_id, selectedDate, employee_id):
        str_date = str(selectedDate)
        sel_date = str_date.split("-")
        day = sel_date[0]
        month = sel_date[1]
        year = sel_date[2]
        calendar_line = request.env['appointment.calendar.line'].sudo().search([('line_id', '=', int(calendar_id))])
        calendar1 = request.env['appointment.calendar'].sudo().browse(int(calendar_id))
        cal_eve = request.env['calendar.event'].search([('employee_ids','in',int(employee_id))])
        new_cal_eve = [calendar1.get_tz_date(datetime.strptime(fields.Datetime.to_string(eve.start), DEFAULT_SERVER_DATETIME_FORMAT), calendar1.tz) for eve in cal_eve]

        slots = []
        for line in calendar_line:
            start_datetime = fields.Datetime.to_string(line.start_datetime)
            date = calendar1.get_tz_date(datetime.strptime(start_datetime, DEFAULT_SERVER_DATETIME_FORMAT), calendar1.tz)
            if int(date.day) == int(day) and int(date.month) == int(month) and int(date.year) == int(year) and date not in new_cal_eve:
                slots.append(str(date.time())[0:5])
        mylst = [s.replace(':', '') for s in slots]
        sorted_slots = [hash[:2] + ':' + hash[2:] for hash in sorted(mylst, key=int)]

        return {'slots': sorted_slots}
