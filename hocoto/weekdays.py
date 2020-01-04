#!/usr/bin/env python3
'''parse commanline arguments'''
# pylint
# vim: tw=100 foldmethod=marker
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements

import datetime

weekdays              = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
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

daynames = {'mon': 'MONDAY',
        'tue': 'TUESDAY',
        'wed': 'WEDNESDAY',
        'thu': 'THURSDAY',
        'fri': 'FRIDAY',
        'sat': 'SATURDAY',
        'sun': 'SUNDAY',
        'tmp': 'WEEKDAY'
        }

