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
    parser.add_argument('--get',           action='store_true',     default=False)
    parser.add_argument('--put',           action='store_true',     default=False)
    parser.add_argument('--day',           choices = weekdays)
    parser.add_argument('--copyfrom',      type=int, default=0)
    parser.add_argument('--copyto',        type=int, default=0)
    parser.add_argument('--test',          type=int, default=0)

    args = parser.parse_args()
    # print(parser.format_values())
    return args, parser

def eventHandler(eventSource, peerId, channel, variableName, value):
    # This callback method is called on Homegear variable changes
    '''event handler'''
    # Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
    # needed when you access non local variables.
    pass
    # print("Event handler called with arguments: source: " + eventSource + \
    #         ";\n     peerId: " + str(peerId) + \
    #         ";\n     channel: " + str(channel) + \
    #         ";\n     variable name: " + variableName + \
    #         ";\n     value: " + str(value))


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
            profile_dict={}
            for day in weekdays:
                profile_dict[day]={}
                day_name = days[day]
                for num in range (1, 14):
                    profile_dict[day]["TEMPERATURE_%s_%d"%(day_name, num)] = device_profile["TEMPERATURE_%s_%d"%(day_name, num)]
                    profile_dict[day]["ENDTIME_%s_%d"%(day_name, num)]     = device_profile["ENDTIME_%s_%d"%(day_name, num)]

            print (F'Copying from "{name_from}" to "{name_to}" for {args.day}')
            hg.putParamset(args.copyto, 0, "MASTER", profile_dict[args.day])
            print ("Done")
            print (json.dumps(profile_dict[args.day], sort_keys=True, indent=4, separators=(',', ': ')))

