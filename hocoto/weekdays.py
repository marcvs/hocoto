#!/usr/bin/env python3
'''parse commanline arguments'''
# pylint
# vim: tw=100 foldmethod=marker
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements

import datetime

# weekdays              = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
weekdays              = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
now = datetime.datetime.now()
days = {'mon': 'MONDAY',
        'tue': 'TUESDAY',
        'wed': 'WEDNESDAY',
        'thu': 'THURSDAY',
        'fri': 'FRIDAY',
        'sat': 'SATURDAY',
        'sun': 'SUNDAY',
        'tmp': 'WEEKDAY',
        'today': now.strftime("%A").upper() }

daynames = {'MON': 'MONDAY',
        'TUE': 'TUESDAY',
        'WED': 'WEDNESDAY',
        'THU': 'THURSDAY',
        'FRI': 'FRIDAY',
        'SAT': 'SATURDAY',
        'SUN': 'SUNDAY',
        'TMP': 'WEEKDAY'
        }
# daynames = {'mon': 'MONDAY',
#         'tue': 'TUESDAY',
#         'wed': 'WEDNESDAY',
#         'thu': 'THURSDAY',
#         'fri': 'FRIDAY',
#         'sat': 'SATURDAY',
#         'sun': 'SUNDAY',
#         'tmp': 'WEEKDAY'
#         }

shortnames = {
        'MONDAY'   : 'MON', 
        'TUESDAY'  : 'TUE', 
        'WEDNESDAY': 'WED', 
        'THURSDAY' : 'THU', 
        'FRIDAY'   : 'FRI', 
        'SATURDAY' : 'SAT', 
        'SUNDAY'   : 'SUN', 
        }
# shortnames = {
#         'MONDAY'   : 'mon',
#         'TUESDAY'  : 'tue',
#         'WEDNESDAY': 'wed',
#         'THURSDAY' : 'thu',
#         'FRIDAY'   : 'fri',
#         'SATURDAY' : 'sat',
#         'SUNDAY'   : 'sun',
#         }
