#!/usr/bin/env python3
'''test'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements

import sys
import os
import logging
import datetime
import sqlite3
import json
import logging
import configargparse

logformat='[%(levelname)s] %(message)s'
logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
logging.basicConfig(level=os.environ.get("LOG", "INFO"), format = logformat)

logger = logging.getLogger(__name__)

dry_run = False
try:
    from homegear import Homegear
except:
    print ('homegear python module not found; running in dry profile_name')
    dry_run = True

def parseOptions():
    '''Parse the commandline options'''
# | ID | Name                      | Address | Serial     | Type | Type String |
# |----+---------------------------+---------+------------+------+-------------|
# | 1  | HM Entkleide OEQ1718409   | 63A25E  | OEQ1718409 | 095  | HM-CC-RT-DN |
# | 2  | HM Wohnzimmer OEQ1711775  | 638586  | OEQ1711775 | 095  | HM-CC-RT-DN |
# # | 3  | HM Kueche vorn OEQ1711363 | 638718  | OEQ1711363 | 095  | HM-CC-RT-DN |
# | 4  | HM Kueche hinten  OEQ1... | 63A260  | OEQ1718411 | 095  | HM-CC-RT-DN |
# | 5  | HM Gaestezimmer OEQ171... | 63A278  | OEQ1718437 | 095  | HM-CC-RT-DN |
# | 6  | HM Bad OEQ1718406         | 63A255  | OEQ1718406 | 095  | HM-CC-RT-DN |
# | 7  | HM Kueche vorn neu        |         |            | 095  | HM-CC-RT-DN |

    path_of_executable = os.path.realpath(sys.argv[0])
    folder_of_executable = os.path.split(path_of_executable)[0]

    config_files = [os.environ['HOME']+'/.config/homematic-profiler.conf',
                    folder_of_executable + '/config/homematic-profiler.conf',
                    '/etc/homematic-profiler.conf']

    parser = configargparse.ArgumentParser(
            default_config_files = config_files,
            description='''test''')
    parser.add('-c', '--my-config', is_config_file=True, help='config file path')
    parser.add_argument('--verbose', '-v',       action="count", default=0, help='Verbosity')
    parser.add_argument('--device',              type=int)
    parser.add_argument('--plot',                action='store_true',     default=False)
    parser.add_argument('--dump',                action='store_true',     default=False)
    parser.add_argument('--get',                 action='store_true',     default=False)
    parser.add_argument('--put',                 action='store_true',     default=False)
    parser.add_argument('--tableview','--table', action='store_true',     default=False)
    parser.add_argument('--day',                 choices = weekdays)
    parser.add_argument('--daynum')
    # parser.add_argument('--day',                 choices = weekdays)
    parser.add_argument('--copy',                action='store_true',     default=False)
    parser.add_argument('--todev',               type=int, default=0)
    parser.add_argument('--fromday',             choices = weekdays)
    parser.add_argument('--today',               choices = weekdays)
    parser.add_argument('--width',               type=int, default=40)

    args = parser.parse_args()
    # print(parser.format_values())
    return args, parser

def eventHandler(eventSource, peerId, channel, variableName, value):
    # This callback method is called on Homegear variable changes
    # Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
    # needed when you access non local variables.
    # print("Event handler called with arguments: source: " + eventSource + \
    #         ";\n     peerId: " + str(peerId) + \
    #         ";\n     channel: " + str(channel) + \
    #         ";\n     variable name: " + variableName + \
    #         ";\n     value: " + str(value))
    pass

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

def ensure_is_list(item):
    '''Make sure we have a list'''
    if isinstance(item, str):
        return [item]
    return item

class HomematicDayProfile():
    '''Class for just one day of homematic'''
    def __init__(self):
        self.profile_dict = {}
        self.time         = []
        self.temp         = []
        self.steps_stored = 0

    def add_step(self, temp, time):
        '''add one step to a profile'''
        self.time.append(time)
        self.temp.append(temp)
        # self.time[self.steps_stored] = time
        # self.temp[self.steps_stored] = temp
        self.steps_stored            += 1

    def get_profile_step(self, step):
        '''get single timestep of a profile'''
        return (self.time[step], self.temp[step])

    def __repr_table__(self):
        rv=''
        for num in range(1, 14):
            total_minutes = self.time[num]
            hours = int(total_minutes / 60)
            minutes = total_minutes - hours*60
            # rv += (F"ENDTIME_{day_name}_{num:<2}: ")
            rv += ("{:>2}:{:0<2}".format(hours,minutes))
            rv += (" - ")
            rv += ("{:<}°C\n".format( str(self.temp[num])))
            if total_minutes == 1440:
                break
        return rv
    def __repr_plot__(self, width = 80):
        '''plot of the temperature graph'''
        rv=''
        time_divisor = int(80*20/width)
        n_time_axes = 180 # all xxx minutes
        if width < 40:
            n_time_axes = 360 # all xxx minutes
        residual = 0.99
        for temp_int in range(220,159,-5):
            cur_time_idx = 1
            temp = temp_int/10.0
            rv += ('{: <5}'.format(temp))

            rv += ('|')
            if (temp % 2 <= 0.1):
                rv += ('\b+')

            for time in range (1, int(1440/time_divisor)):
                dot_made = False
                if self.temp[cur_time_idx] == temp:
                    rv += ('*')
                    dot_made = True
                else:
                    rv += (' ')
                if self.time[cur_time_idx] < time*time_divisor:
                    cur_time_idx += 1
                if not dot_made:
                    if (time-1) % (60/time_divisor) <= residual:
                        rv += ('\b·')
                    if (time) % (n_time_axes/time_divisor) <= residual:
                        rv += ('\b|')
                    if (temp % 2 <= 0.1):
                        rv += ('\b-')
                    if (temp % 2 == 0) and ((time) % (n_time_axes/time_divisor) <= residual):
                        rv += ('\b+')
            rv += ('|')
            if (temp % 2 <= 0.1):
                rv += ('\b+')

            rv += ('\n')

        rv += ('      ')
        for time in range (1, int(1440/time_divisor)):
            hours = int(time*time_divisor/60)
            rv += (' ')
            if (time) % (n_time_axes/time_divisor) <= residual:
                rv += (F"\b\b{hours:>2}")
        rv += ("\b{:>2}".format(24))
        rv += ('\n')
        return rv
    def __repr_dump__(self, day='mon'):
        '''dump a homematic compatible dict for given day'''
        rv_dict={}

        dayname = daynames[day]
        for num in range(1, 14):
            rv_dict[F"ENDTIME_{dayname}_{num}"] = self.time[num-1]
            rv_dict[F"TEMPERATURE_{dayname}_{num}"] = self.temp[num-1]
        return rv_dict



class HomematicProfile():
    '''Class to capture homematic profiles'''
    def __init__(self, profile=None, days=None):
        '''init'''
        self.hm_day_profiles = {}

        if profile is not None:
            self.set_profile(profile, days)

    def set_profile(self, profile, days=None):
        '''add profile to class instance'''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays

        for day in days:
            self.hm_day_profiles[day] = HomematicDayProfile()
            # self.profile_dict[day]={}
            # self.profile_dict[day]['temp']=[]
            # self.profile_dict[day]['time']=[]
            day_name = daynames[day]
            for num in range (1, 14):
                # profile_dict[day][temp][num] = profile["TEMPERATURE_%s_%d"%(day_name, num)]
                # profile_dict[day][time][num] = profile["ENDTIME_%s_%d"%(day_name, num)]
                self.hm_day_profiles[day].add_step(profile["TEMPERATURE_%s_%d"%(day_name, num)],
                                                   profile["ENDTIME_%s_%d"%(day_name, num)])
                # print (F"set: {num}")

    def get_profile(self, days=None):
        '''Get homematic profile for given weekday(s)'''
        output_dict = {}
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            if not self.profile_dict[day]:
                continue
            day_name = daynames[day]
            for num in range (1, 14):
                # output_dict["TEMPERATURE_%s_%d"%(day_name, num)] = self.profile_dict[day]['temp'][num]
                # output_dict["ENDTIME_%s_%d"%(day_name, num)]     = self.profile_dict[day]['time'][num]
                (time, temp) = self.hm_day_profiles[day].get_step(num)
                output_dict["ENDTIME_%s_%d"%(day_name, num)]     = time
                output_dict["TEMPERATURE_%s_%d"%(day_name, num)] = temp

    def __repr_table__(self, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            rv += F"{daynames[day]}\n"
            rv += self.hm_day_profiles[day].__repr_table__()
        return rv

    def __repr_tables_multi__(self):
        rv = ''
        plots = {}
        lines = {}
        # convert plots to lines
        for day in weekdays:
            plots[day] = hm_profile.__repr_table__(days=day)
            lines[day] = plots[day].split('\n')

        maxlines = 0
        for day in weekdays:
            if len(lines[day]) > maxlines:
                maxlines = len(lines[day]) 

        for i in range (0, maxlines-1):
            for day in weekdays:
                try:
                    entry = lines[day][i].rstrip('\n')
                    rv += F"{entry:<15}| "
                except IndexError:
                    rv += "{:<15}| ".format(" ")

            rv += "\n"
        return rv

    def __repr_plot__(self, width=40, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            rv += F"{daynames[day]}\n"
            rv += self.hm_day_profiles[day].__repr_plot__(width = width)
        return rv

    def __repr_plots_multi__(self, width, plots_per_row=3):
        '''mutliple plots in a row'''
        plots = {}
        lines = {}
        do_summary = False
        if plots_per_row == 3:
            do_summary = True
        plots_per_row  -= 1
        blocks_to_plot = int (7 / plots_per_row - 0.1)+1
        rv = ''

        # convert plots to lines
        for day in weekdays:
            plots[day] = hm_profile.__repr_plot__(width=args.width, days=day)
            lines[day] = plots[day].split('\n')

        for blocks in range (0, blocks_to_plot*plots_per_row, plots_per_row+1):
            for i in range (blocks, blocks + plots_per_row + 1):
                try:
                    rv += (("   {:<%d}" % width).format(daynames[weekdays[i]]) )
                except IndexError:
                    pass
            rv += ('\n')
            for line in range (1, len(lines[weekdays[-1]])):
                for i in range (blocks, blocks + plots_per_row + 1):
                    if i < len(lines):
                        rv += (F"{lines[weekdays[i]][line]}  ")
                rv += ("\n")
        return rv

    def __repr_dump__(self, day_in=None, day_out=None):
        if day_in is not None:
            return (self.hm_day_profiles[day_in].__repr_dump__(day_out))
        rv={}
        for day in weekdays:
            temp = self.hm_day_profiles[day].__repr_dump__(day)
            for entry in temp:
                rv[entry] = temp[entry]
                # print (F"  entry: {entry}")
        return rv


weekdays       = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
daynames = {'mon': 'MONDAY',
        'tue': 'TUESDAY',
        'wed': 'WEDNESDAY',
        'thu': 'THURSDAY',
        'fri': 'FRIDAY',
        'sat': 'SATURDAY',
        'sun': 'SUNDAY',
        'tmp': 'WEEKDAY'
        }

def get_fake_paramset():
    '''get a fake profile'''
    t_low = 17
    t_med = 20.5
    t_hig = 21

    profile = {}
    profile["TEMPERATURE_MONDAY_1"]     = t_low
    profile["TEMPERATURE_MONDAY_2"]     = t_hig
    profile["TEMPERATURE_MONDAY_3"]     = t_low
    profile["TEMPERATURE_MONDAY_4"]     = t_med
    profile["TEMPERATURE_MONDAY_5"]     = t_low
    profile["TEMPERATURE_MONDAY_6"]     = t_low
    profile["TEMPERATURE_MONDAY_7"]     = t_low
    profile["TEMPERATURE_MONDAY_8"]     = t_low
    profile["TEMPERATURE_MONDAY_9"]     = t_low
    profile["TEMPERATURE_MONDAY_10"]    = t_low
    profile["TEMPERATURE_MONDAY_11"]    = t_low
    profile["TEMPERATURE_MONDAY_12"]    = t_low
    profile["TEMPERATURE_MONDAY_13"]    = t_low
    profile["TEMPERATURE_TUESDAY_1"]    = t_low
    profile["TEMPERATURE_TUESDAY_2"]    = t_hig
    profile["TEMPERATURE_TUESDAY_3"]    = t_low
    profile["TEMPERATURE_TUESDAY_4"]    = t_med
    profile["TEMPERATURE_TUESDAY_5"]    = t_low
    profile["TEMPERATURE_TUESDAY_6"]    = t_low
    profile["TEMPERATURE_TUESDAY_7"]    = t_low
    profile["TEMPERATURE_TUESDAY_8"]    = t_low
    profile["TEMPERATURE_TUESDAY_9"]    = t_low
    profile["TEMPERATURE_TUESDAY_10"]   = t_low
    profile["TEMPERATURE_TUESDAY_11"]   = t_low
    profile["TEMPERATURE_TUESDAY_12"]   = t_low
    profile["TEMPERATURE_TUESDAY_13"]   = t_low
    profile["TEMPERATURE_WEDNESDAY_1"]  = t_low
    profile["TEMPERATURE_WEDNESDAY_2"]  = t_hig
    profile["TEMPERATURE_WEDNESDAY_3"]  = t_low
    profile["TEMPERATURE_WEDNESDAY_4"]  = t_med
    profile["TEMPERATURE_WEDNESDAY_5"]  = t_low
    profile["TEMPERATURE_WEDNESDAY_6"]  = t_low
    profile["TEMPERATURE_WEDNESDAY_7"]  = t_low
    profile["TEMPERATURE_WEDNESDAY_8"]  = t_low
    profile["TEMPERATURE_WEDNESDAY_9"]  = t_low
    profile["TEMPERATURE_WEDNESDAY_10"] = t_low
    profile["TEMPERATURE_WEDNESDAY_11"] = t_low
    profile["TEMPERATURE_WEDNESDAY_12"] = t_low
    profile["TEMPERATURE_WEDNESDAY_13"] = t_low
    profile["TEMPERATURE_THURSDAY_1"]   = t_low
    profile["TEMPERATURE_THURSDAY_2"]   = t_hig
    profile["TEMPERATURE_THURSDAY_3"]   = t_low
    profile["TEMPERATURE_THURSDAY_4"]   = t_med
    profile["TEMPERATURE_THURSDAY_5"]   = t_low
    profile["TEMPERATURE_THURSDAY_6"]   = t_low
    profile["TEMPERATURE_THURSDAY_7"]   = t_low
    profile["TEMPERATURE_THURSDAY_8"]   = t_low
    profile["TEMPERATURE_THURSDAY_9"]   = t_low
    profile["TEMPERATURE_THURSDAY_10"]  = t_low
    profile["TEMPERATURE_THURSDAY_11"]  = t_low
    profile["TEMPERATURE_THURSDAY_12"]  = t_low
    profile["TEMPERATURE_THURSDAY_13"]  = t_low
    profile["TEMPERATURE_FRIDAY_1"]     = t_low
    profile["TEMPERATURE_FRIDAY_2"]     = t_hig
    profile["TEMPERATURE_FRIDAY_3"]     = t_low
    profile["TEMPERATURE_FRIDAY_4"]     = t_med
    profile["TEMPERATURE_FRIDAY_5"]     = t_low
    profile["TEMPERATURE_FRIDAY_6"]     = t_low
    profile["TEMPERATURE_FRIDAY_7"]     = t_low
    profile["TEMPERATURE_FRIDAY_8"]     = t_low
    profile["TEMPERATURE_FRIDAY_9"]     = t_low
    profile["TEMPERATURE_FRIDAY_10"]    = t_low
    profile["TEMPERATURE_FRIDAY_11"]    = t_low
    profile["TEMPERATURE_FRIDAY_12"]    = t_low
    profile["TEMPERATURE_FRIDAY_13"]    = t_low
    profile["TEMPERATURE_SATURDAY_1"]   = t_low
    profile["TEMPERATURE_SATURDAY_2"]   = t_hig
    profile["TEMPERATURE_SATURDAY_3"]   = t_low
    profile["TEMPERATURE_SATURDAY_4"]   = t_med
    profile["TEMPERATURE_SATURDAY_5"]   = t_low
    profile["TEMPERATURE_SATURDAY_6"]   = t_low
    profile["TEMPERATURE_SATURDAY_7"]   = t_low
    profile["TEMPERATURE_SATURDAY_8"]   = t_low
    profile["TEMPERATURE_SATURDAY_9"]   = t_low
    profile["TEMPERATURE_SATURDAY_10"]  = t_low
    profile["TEMPERATURE_SATURDAY_11"]  = t_low
    profile["TEMPERATURE_SATURDAY_12"]  = t_low
    profile["TEMPERATURE_SATURDAY_13"]  = t_low
    profile["TEMPERATURE_SUNDAY_1"]     = t_low
    profile["TEMPERATURE_SUNDAY_2"]     = t_hig
    profile["TEMPERATURE_SUNDAY_3"]     = t_low
    profile["TEMPERATURE_SUNDAY_4"]     = t_med
    profile["TEMPERATURE_SUNDAY_5"]     = t_low
    profile["TEMPERATURE_SUNDAY_6"]     = t_low
    profile["TEMPERATURE_SUNDAY_7"]     = t_low
    profile["TEMPERATURE_SUNDAY_8"]     = t_low
    profile["TEMPERATURE_SUNDAY_9"]     = t_low
    profile["TEMPERATURE_SUNDAY_10"]    = t_low
    profile["TEMPERATURE_SUNDAY_11"]    = t_low
    profile["TEMPERATURE_SUNDAY_12"]    = t_low
    profile["TEMPERATURE_SUNDAY_13"]    = t_low
    profile["ENDTIME_MONDAY_1"]     = 60*5  + 30
    profile["ENDTIME_MONDAY_2"]     = 60*7  + 0
    profile["ENDTIME_MONDAY_3"]     = 60*16 + 0
    profile["ENDTIME_MONDAY_4"]     = 60*21 + 0
    profile["ENDTIME_MONDAY_5"]     = 60*23 + 0
    profile["ENDTIME_MONDAY_6"]     = 60*24 + 0
    profile["ENDTIME_MONDAY_7"]     = 60*24 + 0
    profile["ENDTIME_MONDAY_8"]     = 60*24 + 0
    profile["ENDTIME_MONDAY_9"]     = 60*24 + 0
    profile["ENDTIME_MONDAY_10"]    = 60*24 + 0
    profile["ENDTIME_MONDAY_11"]    = 60*24 + 0
    profile["ENDTIME_MONDAY_12"]    = 60*24 + 0
    profile["ENDTIME_MONDAY_13"]    = 60*24 + 0
    profile["ENDTIME_TUESDAY_1"]    = 60*5  + 30
    profile["ENDTIME_TUESDAY_2"]    = 60*7  + 0
    profile["ENDTIME_TUESDAY_3"]    = 60*16 + 0
    profile["ENDTIME_TUESDAY_4"]    = 60*21 + 0
    profile["ENDTIME_TUESDAY_5"]    = 60*23 + 0
    profile["ENDTIME_TUESDAY_6"]    = 60*24 + 0
    profile["ENDTIME_TUESDAY_7"]    = 60*24 + 0
    profile["ENDTIME_TUESDAY_8"]    = 60*24 + 0
    profile["ENDTIME_TUESDAY_9"]    = 60*24 + 0
    profile["ENDTIME_TUESDAY_10"]   = 60*24 + 0
    profile["ENDTIME_TUESDAY_11"]   = 60*24 + 0
    profile["ENDTIME_TUESDAY_12"]   = 60*24 + 0
    profile["ENDTIME_TUESDAY_13"]   = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_1"]  = 60*5  + 30
    profile["ENDTIME_WEDNESDAY_2"]  = 60*7  + 0
    profile["ENDTIME_WEDNESDAY_3"]  = 60*16 + 0
    profile["ENDTIME_WEDNESDAY_4"]  = 60*21 + 0
    profile["ENDTIME_WEDNESDAY_5"]  = 60*23 + 0
    profile["ENDTIME_WEDNESDAY_6"]  = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_7"]  = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_8"]  = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_9"]  = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_10"] = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_11"] = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_12"] = 60*24 + 0
    profile["ENDTIME_WEDNESDAY_13"] = 60*24 + 0
    profile["ENDTIME_THURSDAY_1"]   = 60*5  + 30
    profile["ENDTIME_THURSDAY_2"]   = 60*7  + 0
    profile["ENDTIME_THURSDAY_3"]   = 60*16 + 0
    profile["ENDTIME_THURSDAY_4"]   = 60*21 + 0
    profile["ENDTIME_THURSDAY_5"]   = 60*23 + 0
    profile["ENDTIME_THURSDAY_6"]   = 60*24 + 0
    profile["ENDTIME_THURSDAY_7"]   = 60*24 + 0
    profile["ENDTIME_THURSDAY_8"]   = 60*24 + 0
    profile["ENDTIME_THURSDAY_9"]   = 60*24 + 0
    profile["ENDTIME_THURSDAY_10"]  = 60*24 + 0
    profile["ENDTIME_THURSDAY_11"]  = 60*24 + 0
    profile["ENDTIME_THURSDAY_12"]  = 60*24 + 0
    profile["ENDTIME_THURSDAY_13"]  = 60*24 + 0
    profile["ENDTIME_FRIDAY_1"]     = 60*5  + 30
    profile["ENDTIME_FRIDAY_2"]     = 60*7  + 0
    profile["ENDTIME_FRIDAY_3"]     = 60*16 + 0
    profile["ENDTIME_FRIDAY_4"]     = 60*21 + 0
    profile["ENDTIME_FRIDAY_5"]     = 60*23 + 0
    profile["ENDTIME_FRIDAY_6"]     = 60*24 + 0
    profile["ENDTIME_FRIDAY_7"]     = 60*24 + 0
    profile["ENDTIME_FRIDAY_8"]     = 60*24 + 0
    profile["ENDTIME_FRIDAY_9"]     = 60*24 + 0
    profile["ENDTIME_FRIDAY_10"]    = 60*24 + 0
    profile["ENDTIME_FRIDAY_11"]    = 60*24 + 0
    profile["ENDTIME_FRIDAY_12"]    = 60*24 + 0
    profile["ENDTIME_FRIDAY_13"]    = 60*24 + 0
    profile["ENDTIME_SATURDAY_1"]   = 60*5  + 30
    profile["ENDTIME_SATURDAY_2"]   = 60*7  + 0
    profile["ENDTIME_SATURDAY_3"]   = 60*16 + 0
    profile["ENDTIME_SATURDAY_4"]   = 60*21 + 0
    profile["ENDTIME_SATURDAY_5"]   = 60*23 + 0
    profile["ENDTIME_SATURDAY_6"]   = 60*24 + 0
    profile["ENDTIME_SATURDAY_7"]   = 60*24 + 0
    profile["ENDTIME_SATURDAY_8"]   = 60*24 + 0
    profile["ENDTIME_SATURDAY_9"]   = 60*24 + 0
    profile["ENDTIME_SATURDAY_10"]  = 60*24 + 0
    profile["ENDTIME_SATURDAY_11"]  = 60*24 + 0
    profile["ENDTIME_SATURDAY_12"]  = 60*24 + 0
    profile["ENDTIME_SATURDAY_13"]  = 60*24 + 0
    profile["ENDTIME_SUNDAY_1"]     = 60*5  + 30
    profile["ENDTIME_SUNDAY_2"]     = 60*7  + 0
    profile["ENDTIME_SUNDAY_3"]     = 60*16 + 0
    profile["ENDTIME_SUNDAY_4"]     = 60*21 + 0
    profile["ENDTIME_SUNDAY_5"]     = 60*23 + 0
    profile["ENDTIME_SUNDAY_6"]     = 60*24 + 0
    profile["ENDTIME_SUNDAY_7"]     = 60*24 + 0
    profile["ENDTIME_SUNDAY_8"]     = 60*24 + 0
    profile["ENDTIME_SUNDAY_9"]     = 60*24 + 0
    profile["ENDTIME_SUNDAY_10"]    = 60*24 + 0
    profile["ENDTIME_SUNDAY_11"]    = 60*24 + 0
    profile["ENDTIME_SUNDAY_12"]    = 60*24 + 0
    profile["ENDTIME_SUNDAY_13"]    = 60*24 + 0
    return profile


(args, parser) = parseOptions()


# Read data
if not dry_run:
    hg             = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
    device_profile = hg.getParamset(args.device, 0, "MASTER")
    # print (json.dumps(device_profile, sort_keys=True, indent=4, separators=(',', ': ')))
    device_name    = hg.getName(args.device).lstrip('"').rstrip('"')
else:
    device_profile = get_fake_paramset()
    device_name    = "testing"

hm_profile         = HomematicProfile(device_profile)
# print (json.dumps(hm_profile, sort_keys=True, indent=4, separators=(',', ': ')))

print (F"{device_name}\n")
if args.tableview:
    # print (hm_profile.__repr_table__(days=args.day))
    print (hm_profile.__repr_tables_multi__())
# print (hm_profile.__repr_plot__(width=args.width, days=args.day))
if args.plot:
    print (hm_profile.__repr_plots_multi__(width=args.width))

if args.copy:
    if not args.todev:
        args.todev = args.device
    target_device_name = hg.getName(args.todev).lstrip('"').rstrip('"')
    # print (F"Copy from zargs.device} to {args.todev}")
    print (F"Copy from {device_name} to {target_device_name}")
    if not args.fromday:
        # copy all days
        print ("All days")
        target_device_profile = hm_profile.__repr_dump__()
        temp_profile = HomematicProfile(target_device_profile)
        # print (temp_profile.__repr_table__(days=args.fromday))
        print (temp_profile.__repr_plots_multi__(width=args.width))
    elif not args.today:
        print("You must specify --today if you specify --fromday")
        exit (3)
    if args.today:
        print (F"{args.fromday} => {args.today}")
        target_device_profile = hm_profile.__repr_dump__(args.fromday, args.today)
        temp_profile = HomematicProfile(profile=target_device_profile, days=args.today)
        # print (temp_profile.__repr_table__(days=args.today))
        print (temp_profile.__repr_plot__(days=args.today))
    # print (json.dumps(target_device_profile, sort_keys=True, indent=4, separators=(',', ': ')))
    if (args.device == args.todev) and (args.fromday == args.today):
        print ("Cowardly refusing to use target with identical destination")
        exit (6)
    if not dry_run:
        hg.putParamset(args.todev, 0, "MASTER", target_device_profile)
        # pass
        print ("Copy complete")



exit (0)

if args.copy:
    # sanity checking:
    if args.fr == 0:
        args.fr = args.device
        # print ("you must specify a copyfrom device")
    if args.to == 0:
        print ("you must specify a copyto device")
        exit (1)

    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
        name_from      = hg.getName(args.fr).lstrip('"').rstrip('"')
        name_to        = hg.getName(args.to).lstrip('"').rstrip('"')

        if not args.dayfrom:
            print (F'Copying from "{name_from}" to "{name_to}"')
            hg.putParamset(args.copyto, 0, "MASTER", device_profile)
            print ("Done")
        else:
            profile_dict = split_profiles_by_days (device_profile)
            print (F'Copying from "{name_from}" to "{name_to}" for {args.day}')
            hg.putParamset(args.copyto, 0, "MASTER", profile_dict[args.day])
            print ("Done")
            print (json.dumps(profile_dict[args.day], sort_keys=True, indent=4, separators=(',', ': ')))


if args.visualise:
    # sanity checking:
    if not args.device:
        print ("you must specify a device")
        exit (1)
    if args.day:
        view_days = [args.day]
    else:
        view_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    print (F"Days: {view_days}")
    for day in view_days:
        day_name = daynames[day]

        if not dry_run:
            hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
            device_profile = hg.getParamset(args.device, 0, "MASTER")
            device_name    = hg.getName(args.device).lstrip('"').rstrip('"')
        else:
            device_profile = get_fake_paramset()
            device_name    = "fake"

            profile_dict = split_profiles_by_days (device_profile)
            # print (json.dumps(profile_dict[day], sort_keys=True, indent=4, separators=(',', ': ')))
            if args.tableview:
                for num in range(1, 14):
                    total_minutes = profile_dict[day]["ENDTIME_%s_%d"%(day_name, num)]
                    hours = int(total_minutes / 60)
                    minutes = total_minutes - hours*60
                    sys.stdout.write(F"ENDTIME_{day_name}_{num:<2}: ")
                    sys.stdout.write("{:>2}:{:0<2}".format(hours,minutes))
                    sys.stdout.write(" - ")
                    sys.stdout.write("{:<4}\n".format( str(profile_dict[day]["TEMPERATURE_%s_%d"%(day_name, num)] )))
                    if total_minutes == 1440:
                        break

            # time_divisor = 6
            # time_divisor = 12
            time_divisor = 20
            for temp_int in range(220,159,-5):
                cur_time_idx = 1
                temp = temp_int/10.0
                sys.stdout.write('{: <5}'.format(temp))
                for time in range (1, int(1440/time_divisor+2)):
                    dot_made = False
                    if profile_dict[day]["TEMPERATURE_%s_%d"%(day_name, cur_time_idx)] == temp:
                        sys.stdout.write('*')
                        dot_made = True
                    else:
                        sys.stdout.write(' ')
                    if profile_dict[day]["ENDTIME_%s_%d"%(day_name, cur_time_idx)] < time*time_divisor:
                        cur_time_idx += 1
                    if not dot_made:
                        if (time-1) % (60/time_divisor) == 0:
                            sys.stdout.write('\b.')
                        if (time-1) % (180/time_divisor) == 0:
                            sys.stdout.write('\b|')
                        if (temp % 2 == 0):
                            sys.stdout.write('\b-')
                        if (temp % 2 == 0) and ((time-1) % (180/time_divisor) == 0):
                            sys.stdout.write('\b+')
                sys.stdout.write('\n')

            sys.stdout.write('     ')
            for time in range (1, int(1440/time_divisor+2)):
                hours = int(time*time_divisor/60)
                sys.stdout.write(' ')
                # if (time-1) % (60/time_divisor) == 0:
                #     sys.stdout.write('\b.')
                if (time-1) % (180/time_divisor) == 0:
                    sys.stdout.write(F"\b\b{hours:>2}")
                # if (temp % 2 == 0):
                #     sys.stdout.write('\b.')
            sys.stdout.write('\n')
                    

            # for time in range (1, int(1440/time_divisor), 60):
            #     sys.stdout.write('{:<5}'.format(time*time_divisor/60))
