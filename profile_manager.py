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
import datetime
import sqlite3
import json
import logging
import configargparse

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
    parser.add_argument('--verbose', '-v', action="count", default=0, help='Verbosity')
    parser.add_argument('--device',        type=int)
    parser.add_argument('--visualise',     action='store_true',     default=False)
    parser.add_argument('--get',           action='store_true',     default=False)
    parser.add_argument('--put',           action='store_true',     default=False)
    parser.add_argument('--tableview',     action='store_true',     default=False)
    parser.add_argument('--day',           choices = weekdays)
    parser.add_argument('--daynum')
    # parser.add_argument('--day',           choices = weekdays)
    parser.add_argument('--copyfrom',      type=int, default=0)
    parser.add_argument('--copyto',        type=int, default=0)
    parser.add_argument('--test',          type=int, default=0)

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
    profile_dict={}
    for day in weekdays:
        profile_dict[day]={}
        day_name = days[day]
        for num in range (1, 14):
            profile_dict[day]["TEMPERATURE_%s_%d"%(day_name, num)] = device_profile["TEMPERATURE_%s_%d"%(day_name, num)]
            profile_dict[day]["ENDTIME_%s_%d"%(day_name, num)]     = device_profile["ENDTIME_%s_%d"%(day_name, num)]
    return profile_dict

weekdays       = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
days = {'mon': 'MONDAY',
        'tue': 'TUESDAY',
        'wed': 'WEDNESDAY',
        'thu': 'THURSDAY',
        'fri': 'FRIDAY',
        'sat': 'SATURDAY',
        'sun': 'SUNDAY',
        'tmp': 'WEEKDAY'
        }


(args, parser) = parseOptions()

if args.get:
    # sanity checking:
    if not args.device:
        print ("you must specify a device")
        exit (1)

    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
        device_profile = hg.getParamset(args.device, 0, "MASTER")
        # device_profile = hg.getAllConfig()
        print (json.dumps(device_profile, sort_keys=True, indent=4, separators=(',', ': ')))


if args.copyfrom:
    # sanity checking:
    if args.copyto == 0:
        print ("you must specify a copyto device")

    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
        device_profile = hg.getParamset(args.copyfrom, 0, "MASTER")
        name_from      = hg.getName(args.copyfrom).lstrip('"').rstrip('"')
        name_to        = hg.getName(args.copyto).lstrip('"').rstrip('"')


        if not args.day:
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
        view_days = args.day
    else:
        view_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    print (F"Days: {days}")
    for day in view_days:
        print (F"Day: {day}")

        day_name = days[day]

        if not dry_run:
            hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
            device_profile = hg.getParamset(args.device, 0, "MASTER")
            device_name    = hg.getName(args.device).lstrip('"').rstrip('"')

            profile_dict = split_profiles_by_days (device_profile)
            # print (json.dumps(profile_dict[day], sort_keys=True, indent=4, separators=(',', ': ')))
            print (F"{device_name} - {day_name}")
            if args.tableview:
                for num in range(1, 13):
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
                            sys.stdout.write('\b.')
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
