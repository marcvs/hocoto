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
from hocoto.tools import split_profiles_by_days

logformat='[%(levelname)s] %(message)s'
if args.verbose or args.debug:
    logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
if args.debug:
    logging.basicConfig(level=os.environ.get("LOG", "DEBUG"), format = logformat)
else:
    logging.basicConfig(level=os.environ.get("LOG", "INFO"), format = logformat)

logger = logging.getLogger(__name__)


dry_run = False
try:
    from homegear import Homegear
except:
    logger.info('homegear python module not found; running in dry profile_name')
    dry_run = True

####################################################################################################

# Read data
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

hm_profile         = HomematicProfile(device_profile)


if args.dump: # raw dump
    # print (json.dumps(device_profile, sort_keys=True, indent=4, separators=(',', ': ')))
    print (hm_profile.__repr_dump__())
    exit(0)

if args.table:
    # print (hm_profile.__repr_table__(days=args.day))
    print (hm_profile.__repr_tables_multi__())
if args.table_dedup:
    print (hm_profile.__repr_table_dedup__())
# print (hm_profile.__repr_plot__(width=args.width, days=args.day))
if args.plot:
    print (hm_profile.__repr_plots_multi__(width=args.width))
if args.plot:
    print (hm_profile.__repr_plots_multi__(width=args.width))
if args.writetofile:
    # FIXME: write to file named args.writetofile
    with open (args.writetofile, "w") as file:
        file.write (hm_profile.__repr_table_dedup___())
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

exit(0)
