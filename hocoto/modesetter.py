#!/usr/bin/env python3

# pylint 
# vim: tw=100 
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy

import sys
import os
import datetime
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
# | 3  | HM Kueche vorn OEQ1711363 | 638718  | OEQ1711363 | 095  | HM-CC-RT-DN |
# | 4  | HM Kueche hinten  OEQ1... | 63A260  | OEQ1718411 | 095  | HM-CC-RT-DN |
# | 5  | HM Gaestezimmer OEQ171... | 63A278  | OEQ1718437 | 095  | HM-CC-RT-DN |
# | 6  | HM Bad OEQ1718406         | 63A255  | OEQ1718406 | 095  | HM-CC-RT-DN |

    path_of_executable = os.path.realpath(sys.argv[0])
    folder_of_executable = os.path.split(path_of_executable)[0]

    config_files = [os.environ['HOME']+'/.config/homematic-profiler.conf',
                    folder_of_executable + '/config/homematic-profiler.conf',
                    '/etc/homematic-profiler.conf']

    parser = configargparse.ArgumentParser(
            default_config_files = config_files,
            description='''test''')
    parser.add('-c', '--my-config', is_config_file=True, help='config file path')

    parser.add_argument('--verbose',    '-v',       action="count", default=0, help='Verbosity')
    parser.add_argument('--device',     '-d',       type=int, default=-1)
    parser.add_argument('--temp',       '-t',       type=float, default=None)
    parser.add_argument('--dump',                   action='store_true',     default=False)
    parser.add_argument('--mode',       '-m',
        help="0:AUTO-MODE, 1:MANU-MODE,  2:PARTY-MODE, 3:BOOST-MODE",
        type=int, default=None)
    parser.add_argument('--until',      '-u',       type=str, default=None, help='26.11.19:22:33')
    parser.add_argument('--start-in',   '-s',       type=int, default=None, help='hours')

    args = parser.parse_args()
    # print(parser.format_values())
    return args, parser
#

# This callback method is called on Homegear variable changes
def eventHandler(eventSource, peerId, channel, variableName, value):
    '''event handler, unused'''
	# Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
	# needed when you access non local variables.
	# print("Event handler called with arguments: source: " + eventSource + " peerId: " + str(peerId) + "; channel: " + str(channel) + "; variable name: " + variableName + "; value: " + str(value))
    pass


def main():
    (args, parser) = parseOptions()
    hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
    MODES=[ 'AUTO_MODE' ,'MANU_MODE' ,'PARTY_MODE' ,'BOOST_MODE']

    if args.mode:
        print (" Desired mode: {}".format(MODES[args.mode]))

    if (args.device != -1):
        devices = [args.device]
    else:
        devices = range (1, 8)
    print ("+-------+-----+-----------------+------------+------+-------+------+-----------------------+")
    print ("| State | Dev#|  Name           |  Mode      | Temp | Valve | Bat  |                       |")
    print ("+-------+-----+-----------------+------------+------+-------+------+-----------------------+")
    for device in devices:
        try:
            mode = hg.getValue(device, 4, "CONTROL_MODE")
            temp = hg.getValue(device, 4, "SET_TEMPERATURE")
            name = hg.getName(device).lstrip('"').rstrip('"')
            valv = hg.getValue(device, 4, "VALVE_STATE" )
            bat  = hg.getValue(device, 4, "BATTERY_STATE")
        except:
            continue
            pass

        if mode != 2: # All modes but PARTY:
            print("| Curr  | {: ^3} | {: <15} | {: <10} | {: <4} | {: >4}% | {: <4} |                       |".format(device, name, MODES[mode], temp, valv, bat))
        else: # PARTY
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
            print("| Curr  | {: ^3} | {: <15} | {: <10} | {: <4} | {: >4}% | {: <4} | Until: {} {:0>2}:{:0<2} |"\
                    .format(device, name, MODES[mode], temp, valv, bat, px_date, px_h, px_min))


        sth_changed = False

        if args.mode is not None:
            sth_changed = True
            if args.mode == 0:
                if args.verbose:
                    print ('Setting mode: AUTO')
                hg.setValue(device, 4, MODES[args.mode], True)
            if args.mode == 1:
                if args.verbose:
                    print ('Setting mode: MANUAL')
                hg.setValue(device, 4, MODES[args.mode], True)
            if args.mode == 2: ## Party Mode
                if args.verbose:
                    print ('Setting mode: PARTY ')
                p_temp                           = args.temp
                (px_day, px_month, px_year_time) = args.until.split(".")
                (px_year, px_h, px_min)          = px_year_time.split(":")
                now      = datetime.datetime.now()
                ps_day   = int(now.day)
                ps_month = int(now.month)
                ps_year  = int(now.year)
                if ps_year > 1000:
                    ps_year -= 2000
                ps_h     = int(now.hour)
                if args.start_in:
                    ps_h += int(args.start_in)
                ps_min   = int(now.minute)

                px_day   = int(px_day)
                px_month = int(px_month)
                px_year  = int(px_year)
                px_h     = int(px_h)
                px_min   = int(px_min)

                ps_time  = 60*ps_h + ps_min
                px_time  = 60*px_h + px_min

                if args.verbose:
                    print (F'''
                            party_temperature    {p_temp}
                            ps_h                 {ps_h}
                            ps_min               {ps_min}
                            ps_time              {ps_time}
                            ps_month             {ps_month}
                            ps_year              {ps_year}
                            px_h                 {px_h}
                            px_min               {px_min}
                            px_time              {px_time}
                            px_day               {px_day}
                            px_month             {px_month}
                            px_year              {px_year}
                            ''')

                hg.setValue(device, 4, 'PARTY_MODE_SUBMIT',
                    F"{p_temp},{ps_time},{ps_day},{ps_month},{ps_year},{px_time},{px_day},{px_month},{px_year}")
                        # F"8.5,1200,23,11,19,1380,26,11,19")

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

                if args.verbose:
                    print (F'''
                            party_temperature    {p_temp}
                            ps_h                 {ps_h}
                            ps_min               {ps_min}
                            ps_time              {ps_time}
                            ps_month             {ps_month}
                            ps_year              {ps_year}
                            px_h                 {px_h}
                            px_min               {px_min}
                            px_time              {px_time}
                            px_day               {px_day}
                            px_month             {px_month}
                            px_year              {px_year}
                            ''')
    # PARTY_TEMPERATURE PARTY_START_TIME PARTY_START_DAY PARTY_START_MONTH PARTY_START_YEAR PARTY_STOP_TIME PARTY_STOP_DAY PARTY_STOP_MONTH PARTY_STOP_YEAR

            if args.mode == 3: ## Boost Mode
                if args.verbose:
                    print ('Setting mode: BOOST')
                hg.setValue(device, 4, MODES[args.mode], True)

        if args.temp is not None and temp != args.temp:
            sth_changed = True
            hg.setValue(device, 4, "SET_TEMPERATURE", args.temp)

        if sth_changed:
            mode = hg.getValue(device, 4, "CONTROL_MODE")
            temp = hg.getValue(device, 4, "SET_TEMPERATURE")
            valv = hg.getValue(device, 4, "VALVE_STATE" )
            bat  = hg.getValue(device, 4, "BATTERY_STATE")
            if mode != 2: # All modes but PARTY:
                print("| Curr  | {: ^3} | {: <15} | {: <10} | {: <4} | {: >4}% | {: <4} |                       |".format(device, name, MODES[mode], temp, valv, bat))
            else:
                px_date = F"{px_day}.{px_month}.{px_year}"
                print("| Curr  | {: ^3} | {: <15} | {: <10} | {: <4} | {: >4}% | {: <4} | Until: {} {:0>2}:{:0<2} |"\
                    .format(device, name, MODES[mode], temp, valv, bat, px_date, px_h, px_min))
            
            if device != devices[-1]:
                print
                ("+.......+.....+.................+............+......+.......+......+.......................+")
    print ("+-------+-----+-----------------+------------+------+-------+------+-----------------------+")

if __name__ == '__main__':
    main()
