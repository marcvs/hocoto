#!/usr/bin/env python3
'''homematic day profile'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements
import logging
from hocoto.weekdays import weekdays, days, daynames

logger = logging.getLogger(__name__)
def split_profiles_by_days(profile):
    '''split profiles by days'''
    profile_dict={}
    for day in weekdays:
        profile_dict[day]={}
        day_name = daynames[day]
        for num in range (1, 14):
            profile_dict[day]["TEMPERATURE_%s_%d"%(day_name, num)] = device_profile["TEMPERATURE_%s_%d"%(day_name, num)]
            profile_dict[day]["ENDTIME_%s_%d"%(day_name, num)]     = device_profile["ENDTIME_%s_%d"%(day_name, num)]
    return profile_dict
