#!/usr/bin/env python3
'''test'''
# pylint # {{{
# vim: tw=100 foldmethod=marker
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements
# }}}


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

def parseOptions():# {{{
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

    parser.add_argument('--verbose', '-v', action="count", default=0, help='Verbosity')
    parser.add_argument('all_args',        nargs='*')
    parser.add_argument('--logfile',       default='/tmp/test-py.log')
    parser.add_argument('--loglevel',      default='debug')
    parser.add_argument('--device',        type=int)
    parser.add_argument('--day',           choices = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
    parser.add_argument('--profile_name',  '--mode',            choices = allowed_profile_names)
    parser.add_argument('--put',           action='store_true', default=False)
    parser.add_argument('--get',           action='store_true', default=False)
    parser.add_argument('--db-file',       default='/var/tmp/homematic_profile.db')
    parser.add_argument('--t-lo',          type=float,            default=17)
    parser.add_argument('--t-med',         type=float,            default=18)
    parser.add_argument('--t-high',        type=float,            default=20)
    parser.add_argument('--t-hottt',       type=float,            default=21)

    args = parser.parse_args()
    # print(parser.format_values())
    return args, parser
#}}}
def eventHandler(eventSource, peerId, channel, variableName, value):# {{{
    # This callback method is called on Homegear variable changes
    '''event handler'''
    # Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
    # needed when you access non local variables.
    print("Event handler called with arguments: source: " + eventSource + \
            ";\n     peerId: " + str(peerId) + \
            ";\n     channel: " + str(channel) + \
            ";\n     variable name: " + variableName + \
            ";\n     value: " + str(value))
# }}}
def profile_generator(profilename, day_short_name, temps):# {{{
    '''Generate profiles for given weekday'''
    now = datetime.datetime.now()
    days = {'mon': 'MONDAY',
            'tue': 'TUESDAY',
            'wed': 'WEDNESDAY',
            'thu': 'THURSDAY',
            'fri': 'FRIDAY',
            'sat': 'SATURDAY',
            'sun': 'SUNDAY',
            'today': now.strftime("%A").upper() }
    day_name = days[day_short_name]

    t_lo    = temps['t_lo']
    t_med   = temps['t_med']
    t_high  = temps['t_high']
    t_hottt = temps['t_hottt']

    # initialise profiles:
    profiles={}
    for apn in allowed_profile_names:
        profiles[apn]={}
        profiles[apn]['temp']={}
        profiles[apn]['time']={}
        for i in range (0,13):
            profiles[apn]['temp'][i] = t_lo   ; profiles[apn]['time'][i] = 60* 24 + 0


    profiles['a']['temp'][0]   = t_lo   ; profiles['a']['time'][0]   = 60* 16 + 0
    profiles['a']['temp'][1]   = t_high ; profiles['a']['time'][1]   = 60* 24 + 0
    profiles['a']['temp'][2]   = t_lo   ; profiles['a']['time'][2]   = 60* 24 + 0

    profiles['ma']['temp'][0]  = t_lo   ; profiles['ma']['time'][0]  = 60*  6 + 0
    profiles['ma']['temp'][1]  = t_high ; profiles['ma']['time'][1]  = 60*  8 + 0
    profiles['ma']['temp'][2]  = t_lo   ; profiles['ma']['time'][2]  = 60* 16 + 0
    profiles['ma']['temp'][3]  = t_med  ; profiles['ma']['time'][3]  = 60* 23 + 0
    profiles['ma']['temp'][4]  = t_lo   ; profiles['ma']['time'][4]  = 60* 24 + 0

    profiles['fma']['temp'][0] = t_lo   ; profiles['fma']['time'][0] = 60*  5 + 00
    profiles['fma']['temp'][1] = t_high ; profiles['fma']['time'][1] = 60*  9 + 0
    profiles['fma']['temp'][2] = t_lo   ; profiles['fma']['time'][2] = 60* 17 + 0
    profiles['fma']['temp'][3] = t_med  ; profiles['fma']['time'][3] = 60* 21 + 00
    profiles['fma']['temp'][4] = t_high ; profiles['fma']['time'][4] = 60* 23 + 0
    profiles['fma']['temp'][5] = t_lo   ; profiles['fma']['time'][5] = 60* 24 + 0

    profiles['t']['temp'][0]   = t_lo   ; profiles['t']['time'][0]   = 60*  8 + 0
    profiles['t']['temp'][1]   = t_high ; profiles['t']['time'][1]   = 60* 10 + 0
    profiles['t']['temp'][2]   = t_med  ; profiles['t']['time'][2]   = 60* 18 + 0
    profiles['t']['temp'][3]   = t_lo   ; profiles['t']['time'][3]   = 60* 24 + 0

    profiles['ta']['temp'][0]  = t_lo   ; profiles['ta']['time'][0]  = 60*  8 + 0
    profiles['ta']['temp'][1]  = t_med  ; profiles['ta']['time'][1]  = 60* 19 + 30
    profiles['ta']['temp'][2]  = t_high ; profiles['ta']['time'][2]  = 60* 23 + 50
    profiles['ta']['temp'][3]  = t_lo   ; profiles['ta']['time'][3]  = 60* 24 + 0

    params={}
    for i in range(0,13):
        params["TEMPERATURE_%s_%d"%(day_name, i+1)] = profiles[profilename]['temp'][i]
        params["ENDTIME_%s_%d"%(day_name, i+1)]     = profiles[profilename]['time'][i]
    return(params)
# }}}


# Global variables
allowed_profile_names = ["fma", "ma", "t", "ta", "a"]
################### sqlite ##############
def dict_factory(cursor, row):# {{{
    '''helper for json export from sqlite'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# }}}
def init_sqlite_tables(db_file):# {{{
    '''helper to initialise sql db'''
    # Setup SQL tables
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        cur.execute('''create table if not exists hp_device_day_profile_map'''
            '''(device INTEGER, weekday TEXT, profile TEXT,
            t_lo REAL, t_med REAL, t_high REAL, t_hottt REAL)''')
        conn.commit()
        conn.close()

    except sqlite3.OperationalError as e:
        print ("SQL Create error: " + str(e))
        raise
    # self.db_was_initialised = True
# }}}
def store_entry_in_db(db_file, device, day, profile, temps):# {{{
    '''Store profile for given weekday and device'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        query = '''delete from hp_device_day_profile_map where device=%s and weekday='%s' ''' %\
                (device, day);
        # print ("Query in store_entry_in_db: " + query)
        cur.execute(query)
        conn.commit()
        query = '''insert into hp_device_day_profile_map values (%d, '%s', '%s', %5.2f, %5.2f, %5.2f, %5.2f)''' %\
                (device, day, profile, temps['t_lo'], temps['t_med'], temps['t_high'], temps['t_hottt'])
        # print ("Query in store_entry_in_db: " + query)
        cur.execute(query)
        conn.commit()

    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
        return(False)
    conn.close()
    return(True)
    # }}}
# }}}
def read_entry_from_db(db_file, device, day):# {{{
    '''Read some or all entries from sqlite'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        query = '''select * from hp_device_day_profile_map where device=%d and weekday='%s' ''' %\
            (device, day)
        # print ("Query in read_entry_from_db: " + query)
        cur.execute(query)
        conn.commit()
        allentries = cur.fetchall()
        if len(allentries) > 1:
            print ("Warning; Query >>%s<< yielded %d entries; Expected only one. Using last one" %
                (query, len(allentries)))

    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
    conn.close()
    # print ("SQL Result: %s" % str(allentries))
    temps            = {}
    temps['t_lo']    = allentries[-1]['t_lo']
    temps['t_med']   = allentries[-1]['t_med']
    temps['t_high']  = allentries[-1]['t_high']
    temps['t_hottt'] = allentries[-1]['t_hottt']
    return (allentries[-1]['profile'], temps)

    # }}}
# }}}
################### /sqlite ##############


################## MAIN ########################
(args, parser) = parseOptions()
if dry_run:
    args.verbose += 1

# Setup logging{{{
logformat = "{%(asctime)s %(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s"
loglevel = logging.getLevelName(args.loglevel.upper())
logging.basicConfig(level=loglevel, format=logformat, filename=args.logfile)
logging.debug('\nhomematirc_profiler- v.0.0.2')
# }}}
# logging.info(parser.format_values())

init_sqlite_tables(args.db_file)

if args.put:# {{{
    # sanity checking:
    if args.device is None:
        print("device is not specified but required when using --put")
        exit(2)
    if args.day is None:
        print("day is not specified but required when using --put")
        exit(2)
    if args.profile_name is None:
        print("profile_name is not specified but required when using --put")
        exit(1)

    temps = {}
    temps['t_lo']    = args.t_lo
    temps['t_med']   = args.t_med
    temps['t_high']  = args.t_high
    temps['t_hottt'] = args.t_hottt

    store_entry_in_db(args.db_file, args.device, args.day, args.profile_name, temps)

    profile = profile_generator(args.profile_name, args.day, temps)

    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)

        # in_params = hg.getParamset(1, 0, "MASTER")
        # setattr(params, "TEMPERATURE_MONDAY_4", 11)

        hg.putParamset(args.device, 0, "MASTER", profile)
# }}}
if args.get: # {{{
    profile_name, (temps) = read_entry_from_db(args.db_file, args.device, args.day)
    print (profile_name)

    profile = profile_generator(profile_name, args.day, temps)

    if args.verbose:
        print (json.dumps(profile, sort_keys=False, indent=4, separators=(',', ': ')))

# }}}
