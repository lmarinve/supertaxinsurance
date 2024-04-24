# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Appointment Calendar',
    'version': '16.0.1.2',
    'summary': 'Calendar appointment booking with a strong backend and a very intuitive web UI | appointment | website booking | booking calendar | Slot Booking | Online Booking | Online Meeting | Schedule Meeting',
    'description': """
Appointment Calendar
================================
    """,
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'images': ['static/description/banner.jpg'],
    'category': 'Website/Website',
    'depends': ['website', 'mail', 'calendar', 'contacts'],
    'data': [
        'data/appointment_data.xml',
        'security/ir.model.access.csv',
        'views/appointment_calendar_view.xml',
        'views/hr_employee_view.xml',
        'views/appointment.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'appointment_calendar/static/lib/datetime/css/datepicker.css',
            'appointment_calendar/static/lib/datetime/js/bootstrap-datepicker.js',
            'appointment_calendar/static/src/css/appointment.css',
            'appointment_calendar/static/src/js/appointment.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 110,
    'currency': 'EUR',
}
