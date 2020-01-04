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
from hocoto.parse_options_manager import args
from hocoto.weekdays import weekdays, days, daynames
from hocoto.fake_paramset import get_fake_paramset
from hocoto.homematic_event_handler import eventHandler
from hocoto.homematic_day_profile import HomematicDayProfile
from hocoto.homematic_profile import HomematicProfile

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




####################################################################################################
####################################################################################################

# Read data
dp = []
if args.readfromfile:
    hm_day_profile = HomematicDayProfile()
    hm_day_profile.read_from_file(args.readfromfile, args.profilename)
    exit (0)
elif not dry_run:
    hg             = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
    device_profile = hg.getParamset(args.device, 0, "MASTER")
    device_name    = hg.getName(args.device).lstrip('"').rstrip('"')
else:
    device_profile = get_fake_paramset()
    device_name    = "testing"

print (F" {device_name}\n"+("{:=^%d}"%(len(device_name)+2)).format(''))

if args.dump: # raw dump
    print (json.dumps(device_profile, sort_keys=True, indent=4, separators=(',', ': ')))
    exit(0)

hm_profile         = HomematicProfile(device_profile)

if args.table:
    # print (hm_profile.__repr_table__(days=args.day))
    # print (hm_profile.__repr_tables_multi__())
    print (hm_profile.__repr_table_dedup__())
# print (hm_profile.__repr_plot__(width=args.width, days=args.day))
if args.plot:
    print (hm_profile.__repr_plots_multi__(width=args.width))
if args.writetofile:
    # FIXME: write to file named args.writetofile
    with open (args.writetofile, "w") as file:
        file.write (hm_profile.__repr_table__())
    exit (0)

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

hg.exit()


exit (0)

if None:
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
                if args.table:
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
