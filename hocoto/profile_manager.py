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
from sys import stdout
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

def main():

    dry_run = False
    try:
        from homegear import Homegear
    except:
        logger.info('homegear python module not found; running in dry profile_name')
        dry_run = True

    ####################################################################################################
    # defaults:
    device_name = ""

    if not dry_run:
        hg             = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
        
    MODES=[ 'AUTO_MODE' ,'MANU_MODE' ,'PARTY_MODE' ,'BOOST_MODE']
    FAULTS= [ 'NO_FAULT', 'VALVE_TIGHT', 'ADJUSTING_RANGE_TOO_LARGE', 
            'ADJUSTING_RANGE_TOO_SMALL', 'COMMUNICATION_ERROR', 
            'UNDFINED', 'LOWBAT', 'VALVE_ERROR_POSITION']
# 0 = NO_FAULT (Standard)
# 1 = VALVE_TIGHT
# 2 = ADJUSTING_RANGE_TOO_LARGE
# 3 = ADJUSTING_RANGE_TOO_SMALL
# 4 = COMMUNICATION_ERROR
# 5 = UNDFINED
# 6 = LOWBAT
# 7 = VALVE_ERROR_POSITION

    ####################
    # Normalise device names:
    device_names = {}
    device_mode  = {}
    device_temp  = {}
    device_valv  = {}
    device_bat   = {}
    device_fault = {}
    if not dry_run:
        for i in range (1, args.max_devices):
            device = i
            try:
                device_names[i] = hg.getName(device).lstrip('"').rstrip('"')
                # device_name[i]  = hg.getName(device).lstrip('"').rstrip('"')
                device_mode[i]  = hg.getValue(device, 4, "CONTROL_MODE")
                device_temp[i]  = hg.getValue(device, 4, "SET_TEMPERATURE")
                device_valv[i]  = hg.getValue(device, 4, "VALVE_STATE" )
                device_bat[i]   = hg.getValue(device, 4, "BATTERY_STATE")
                device_fault[i] = hg.getValue(device, 4, "FAULT_REPORTING")
            except: 
                pass
    else:
        for i in range (1, 10):
                device_names[i] = F"device_{i}"
                device_mode[i]  = 1
                device_temp[i]  = 2
                device_valv[i]  = 3
                device_bat[i]   = 4
                device_fault[i] = 5
        device_names[1] = "test"

    def device_name_to_num(dev_name_or_num, device_names):
        '''return a numerical version of a device specification'''
        try:
            return int(dev_name_or_num)
        except:
            pass
        if type(device_name) == type(""): # we have a named device, lets replace it with the correct number:
            for cmplen in range (len(dev_name_or_num), 0, -1):
                for (d_num, d_nam) in device_names.items():
                    if dev_name_or_num[0:cmplen].lower() ==  d_nam[0:cmplen].lower():
                        return (d_num)
        print ("Unable to find specified device '{dev_name_or_num}'")
        exit(5)
        return (False)

    if args.device:
        args.device = device_name_to_num(args.device, device_names)
        
    if args.todev:
        args.todev = device_name_to_num(args.todev, device_names)

    if args.temp: 
        if not args.device:
            print ("Device not specified device")
            exit(6)
            return (False)
        hg.setValue(args.device, 4, "SET_TEMPERATURE", args.temp)

    if args.mode is not None:
        if not args.device:
            print ("Device not specified device")
            exit(6)
            return (False)
        hg.setValue(args.device, 4, MODES[args.mode], True)
        device_mode[args.device]  = hg.getValue(args.device, 4, "CONTROL_MODE")
        args.list = True

    ####################
    # list only  (taken from modesetter)
    if args.list:
        print ("+-----+-----------------+------------+------+-------+------+---------------------------+")
        print ("| Dev#|  Name           |  Mode      | Temp | Valve | Bat  |                           |")
        print ("+-----+-----------------+------------+------+-------+------+---------------------------+")
        for i in range (1, args.max_devices):
            device = i
            try:
                name    = device_names[i]
                mode    = device_mode[i]
                temp    = device_temp[i]
                valv    = device_valv[i]
                bat     = device_bat[i]
                comment = ""
                fault   = device_fault[i]
                if fault != 0:
                    comment = F"{FAULTS[fault]}"
            except:
                continue
                pass

            if device == args.device:
                stdout.write ("|<<{:<^2} |".format(device))
                comment = "Selected Input"
            elif device == args.todev:
                stdout.write ("|>>{:>^2} |".format(device))
                comment = "Output"
            else:
                stdout.write ("|  {: ^2} |".format(device))
            if mode != 2: # All modes but PARTY:
                print(" {: <15} | {: <10} | {: <4} | {: >4}% | {: <4} | {: <25} |".\
                        format(name, MODES[mode], temp, valv, bat, comment))
            else: # PARTY
                if not dry_run:
                    party_temperature = hg.getValue(device, 4, 'PARTY_TEMPERATURE')
                    ps_time           = hg.getValue(device, 4, 'PARTY_START_TIME')
                    ps_day            = hg.getValue(device, 4, 'PARTY_START_DAY')
                    ps_month          = hg.getValue(device, 4, 'PARTY_START_MONTH')
                    ps_year           = hg.getValue(device, 4, 'PARTY_START_YEAR')
                    px_time           = hg.getValue(device, 4, 'PARTY_STOP_TIME')
                    px_day            = hg.getValue(device, 4, 'PARTY_STOP_DAY')
                    px_month          = hg.getValue(device, 4, 'PARTY_STOP_MONTH')
                    px_year           = hg.getValue(device, 4, 'PARTY_STOP_YEAR')

                    ps_h = int(ps_time/60)
                    ps_min = ps_time - ps_h * 60
                    px_h = int(px_time/60)
                    px_min = px_time - px_h * 60

                    px_date = F"{px_day}.{px_month}.{px_year}"
                    print(" {: <15} | {: <10} | {: <4} | {: >4}% | {: <4} | Until: {} {:0>2}:{:0<2} |"\
                            .format(name, MODES[mode], temp, valv, bat, px_date, px_h, px_min))
        print ("+-----+-----------------+------------+------+-------+------+---------------------------+\n")

    ####################
    # Read data
    if args.readfromfile:
        hm_profile = HomematicProfile()
        hm_profile.read_from_file(args.readfromfile)
        device_name    = F'Input from file "{args.readfromfile}"'
        args.copy      = True

    elif not dry_run:
        if not args.device:
            # print ("You should specify a device (or a file)")
            # without a device specified there's not more we can do here
            exit (0)
        device_profile = hg.getParamset(args.device, 0, "MASTER")
        device_name    = hg.getName(args.device).lstrip('"').rstrip('"')
        hm_profile     = HomematicProfile(device_profile)
    else:
        device_profile = get_fake_paramset()
        device_name    = "testing"
        hm_profile     = HomematicProfile(device_profile)

    print (F" {device_name}\n"+("{:=^%d}"%(len(device_name)+2)).format(''))

    if args.dump: # raw dump
        # print (json.dumps(device_profile, sort_keys=True, indent=4, separators=(',', ': ')))
        print (hm_profile.__repr_dump__())
        exit(0)

    if args.table:
        # print (hm_profile.__repr_table__(days=args.day))
        print (hm_profile.__repr_tables_multi__())
    if args.table_dedup:
        print (hm_profile.__repr_table_dedup__())
    if args.plot:
        if args.day:
            print (hm_profile.__repr_plot__(width=args.width, days=args.day))
        else:
            print (hm_profile.__repr_plots_multi__(width=args.width))
    if args.writetofile:
        with open (args.writetofile, "w") as file:
            file.write (hm_profile.__repr_table_dedup_all__())
        exit (0)

    if args.copy: # copy from one device to another
        if not args.todev:
            print ("No target device specified")
            exit (2)
        if not dry_run:
            target_device_name = hg.getName(args.todev).lstrip('"').rstrip('"')
        else:
            target_device_name = "Testing-Target"
        # print (F"Copy from zargs.device} to {args.todev}")
        print (F"Copying from {device_name} to {target_device_name}")
        if not args.fromday:
            # copy all days
            print ("All days")
            target_device_profile = hm_profile.__repr_dump__()
            temp_profile = HomematicProfile(target_device_profile)
            # print (temp_profile.__repr_table__(days=args.fromday))
            # print (temp_profile.__repr_plots_multi__(width=args.width))
        elif not args.today:
            print("You must specify --today if you specify --fromday")
            exit (3)
        if args.today:
            if not args.fromday:
                print("You must specify --fromday if you specify --today")
                exit (3)
            print (F"{args.fromday} => {args.today}")
            target_device_profile = hm_profile.__repr_dump__(args.fromday, args.today)
            temp_profile = HomematicProfile(profile=target_device_profile, days=args.today)
            # print (temp_profile.__repr_table__(days=args.today))
            print (temp_profile.__repr_plot__(days=args.today))
        # print (json.dumps(target_device_profile, sort_keys=True, indent=4, separators=(',', ': ')))
        if (args.device == args.todev) and (args.fromday == args.today) and args.today is not None:
            print ("Cowardly refusing to use target with identical destination")
            exit (6)
        if not dry_run:
            hg.putParamset(args.todev, 0, "MASTER", target_device_profile)
            # pass
            print ("Copy complete")

if __name__ == '__main__':
    main()
