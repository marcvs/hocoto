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
    parser.add_argument('all_args',        nargs='*')
    parser.add_argument('--logfile',       default='homematic_profiler.log')
    parser.add_argument('--loglevel',      default='debug')
    parser.add_argument('--device',        type=int)
    parser.add_argument('--day',           choices = weekdays)
    parser.add_argument('--profile_name',  '--mode',            choices = allowed_profile_names)
    parser.add_argument('--put',           action='store_true',     default=False)
    parser.add_argument('--put-t',         action='store_true',     default=False)
    parser.add_argument('--put-all',       action='store_true',     default=False)
    parser.add_argument('--get',           action='store_true',     default=False)
    parser.add_argument('--get-t',         action='store_true',     default=False)
    parser.add_argument('--get-all',       action='store_true',     default=False)
    parser.add_argument('--device-get-t',  action='store_true',     default=False)
    parser.add_argument('--pull-from-device', action='store_true',  default=False)
    parser.add_argument('--create-profile',                         default=None)
    parser.add_argument('--create-all-profiles',action='store_true',default=None)
    parser.add_argument('--get-profile',                            default=None)
    parser.add_argument('--db-file',       default='/var/tmp/homematic_profile.db')
    parser.add_argument('--t-lo',          type=float,              default=0.0)
    parser.add_argument('--t-med',         type=float,              default=0.0)
    parser.add_argument('--t-high',        type=float,              default=0.0)
    parser.add_argument('--t-hottt',       type=float,              default=0.0)

    args = parser.parse_args()
    # print(parser.format_values())
    return args, parser
#}}}
def eventHandler(eventSource, peerId, channel, variableName, value):# {{{
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
# }}}
def profile_generator(profilename, day_short_name, temps):# {{{
    '''Generate profiles for given weekday'''
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
    profiles['a']['temp'][1]   = t_med  ; profiles['a']['time'][1]   = 60* 17 + 0
    profiles['a']['temp'][2]   = t_high ; profiles['a']['time'][2]   = 60* 24 + 0
    profiles['a']['temp'][3]   = t_lo   ; profiles['a']['time'][3]   = 60* 24 + 0

    profiles['ma']['temp'][0]  = t_lo   ; profiles['ma']['time'][0]  = 60*  6 + 0
    profiles['ma']['temp'][1]  = t_high ; profiles['ma']['time'][1]  = 60*  8 + 0
    profiles['ma']['temp'][2]  = t_lo   ; profiles['ma']['time'][2]  = 60* 16 + 0
    profiles['ma']['temp'][3]  = t_med  ; profiles['ma']['time'][3]  = 60* 23 + 0
    profiles['ma']['temp'][4]  = t_lo   ; profiles['ma']['time'][4]  = 60* 24 + 0

    profiles['fma']['temp'][0] = t_lo   ; profiles['fma']['time'][0] = 60*  5 + 0
    profiles['fma']['temp'][1] = t_high ; profiles['fma']['time'][1] = 60*  8 + 0
    profiles['fma']['temp'][2] = t_lo   ; profiles['fma']['time'][2] = 60* 17 + 0
    profiles['fma']['temp'][3] = t_med  ; profiles['fma']['time'][3] = 60* 21 + 0
    profiles['fma']['temp'][4] = t_high ; profiles['fma']['time'][4] = 60* 23 + 0
    profiles['fma']['temp'][5] = t_lo   ; profiles['fma']['time'][5] = 60* 24 + 0

    profiles['t']['temp'][0]   = t_lo   ; profiles['t']['time'][0]   = 60*  8 + 0
    profiles['t']['temp'][1]   = t_high ; profiles['t']['time'][1]   = 60* 10 + 0
    profiles['t']['temp'][2]   = t_med  ; profiles['t']['time'][2]   = 60* 18 + 0
    profiles['t']['temp'][3]   = t_lo   ; profiles['t']['time'][3]   = 60* 24 + 0

    profiles['ta']['temp'][0]  = t_lo   ; profiles['ta']['time'][0]  = 60*  8 + 0
    profiles['ta']['temp'][1]  = t_high ; profiles['ta']['time'][1]  = 60* 21 + 0
    profiles['ta']['temp'][2]  = t_med  ; profiles['ta']['time'][2]  = 60* 22 + 0
    profiles['ta']['temp'][3]  = t_lo   ; profiles['ta']['time'][3]  = 60* 24 + 0

    profiles['o']['temp'][0]  = t_lo   ; profiles['o']['time'][0]  = 60*  1 + 0
    profiles['o']['temp'][1]  = t_lo   ; profiles['o']['time'][1]  = 60* 24 + 0

    params={}
    for i in range(0,13):
        params["TEMPERATURE_%s_%d"%(day_name, i+1)] = profiles[profilename]['temp'][i]
        params["ENDTIME_%s_%d"%(day_name, i+1)]     = profiles[profilename]['time'][i]
    return(params)
# }}}

# Global variables{{{
allowed_profile_names = ["fma", "ma", "t", "ta", "a", "o"]
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
default_t_lo          = 17.0
default_t_med         = 19.0
default_t_high        = 20.0
default_t_hottt       = 21.0
# }}}
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
        # cur.execute('''create table if not exists hp_device_day_profile_map'''
        #     '''(device INTEGER, weekday TEXT, profile TEXT,
        #     t_lo REAL, t_med REAL, t_high REAL, t_hottt REAL)''')
        cur.execute('''create table if not exists hp_device_day_profile_map'''
            '''(device INTEGER, weekday TEXT, profile TEXT)''')
        conn.commit()
        cur.execute('''create table if not exists hp_device_temperature_map'''
            '''(device INTEGER, t_lo REAL, t_med REAL, t_high REAL, t_hottt REAL)''')
        conn.commit()
        cur.execute('''create table if not exists profile_names'''
            '''(name TEXT)''')
        conn.commit()
        cur.execute('''create table if not exists profiles'''
            '''(profile_id INTEGER, number INTEGER, temp TEXT, time INTEGER)''')
        conn.commit()
        conn.close()

    except sqlite3.OperationalError as e:
        print ("SQL Create error: " + str(e))
        raise
    # self.db_was_initialised = True
# }}}
def store_profile_entry_in_db(db_file, device, day, profile):# {{{
    '''Store profile for given weekday and device'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        # hp_device_day_profile_map
        query = '''update hp_device_day_profile_map set device=%d, weekday='%s', '''\
                '''profile='%s' where device=%d and weekday='%s' ''' %\
                (device, day, profile, device, day)
        cur.execute(query)
        conn.commit()
        rows=cur.rowcount
        if cur.rowcount == 0:
            query = '''insert into hp_device_day_profile_map values (%d, '%s', '%s')''' %\
                    (device, day, profile)
            cur.execute(query)
            conn.commit()
    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
        return(False)
    conn.close()
    return(True)
    # }}}
# }}}
def store_temps_entry_in_db(db_file, device, temps):# {{{
    '''Store profile for given weekday and device'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        # hp_device_temperature_map
        query = '''update hp_device_temperature_map set device=%d, t_lo=%5.2f, t_med=%5.2f, '''\
                '''t_high=%5.2f, t_hottt=%5.2f WHERE device=%d''' %\
                (device, temps['t_lo'], temps['t_med'], temps['t_high'], temps['t_hottt'], device)
        cur.execute(query)
        conn.commit()
        rows=cur.rowcount
        if cur.rowcount == 0:
            query = '''insert into hp_device_temperature_map values (%d, %5.2f, %5.2f, %5.2f, %5.2f)''' %\
                    (device, temps['t_lo'], temps['t_med'], temps['t_high'], temps['t_hottt'])
            cur.execute(query)
            conn.commit()
            rows=cur.rowcount
    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
        return(False)
    conn.close()
    return(True)
    # }}}
# }}}
def read_profile_entry_from_db(db_file, device, day):# {{{
    '''Read some or all entries from sqlite'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        # query = '''select * from hp_device_day_profile_map where device=%d and weekday='%s' ''' %\
        #     (device, day)
        # print ("Query in read_entry_from_db: " + query)
        query = '''select * from hp_device_day_profile_map where device=%d and weekday='%s' ''' %\
            (device, day)
        # logging.info(query)
        cur.execute(query)
        conn.commit()
        allentries = cur.fetchall()
        if len(allentries) > 1:
            print ("Warning; Query >>%s<< yielded %d entries; Expected only one. Using last one" %
                (query, len(allentries)))
        # logging.info(str(allentries))
    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
    conn.close()
    if allentries == []:
        return ('ma')
    return (allentries[-1]['profile'])

    # }}}
# }}}
def read_temps_entry_from_db(db_file, device):# {{{
    '''Read some or all entries from sqlite'''
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # do sqlite query {{{
    try:
        query = '''select * from hp_device_temperature_map where device=%d ''' % (device)
        cur.execute(query)
        conn.commit()
        all_temp_entries = cur.fetchall()
        if len(all_temp_entries) > 1:
            print ("Warning; Query >>%s<< yielded %d entries; Expected only one. Using last one" %
                (query, len(all_temp_entries)))

    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))
    conn.close()
    # print ("SQL Result: %s" % str(allentries))
    temps            = {}
    try:
        temps['t_lo']    = all_temp_entries[-1]['t_lo']
    except IndexError:
        temps['t_lo']    = default_t_lo
    try:
        temps['t_med']   = all_temp_entries[-1]['t_med']
    except IndexError:
        temps['t_med']    = default_t_med
    try:
        temps['t_high']  = all_temp_entries[-1]['t_high']
    except IndexError:
        temps['t_high']    = default_t_high
    try:
        temps['t_hottt'] = all_temp_entries[-1]['t_hottt']
    except IndexError:
        temps['t_hottt']    = default_t_hottt
    return (temps)
    # }}}
# }}}

def get_profile_id_by_name(db_file, profile_name):# {{{
    # Setup SQL connection # {{{
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    # }}}
    # store profile name and get its ID
    try:
        query = '''update profile_names set name='%s' WHERE name='%s' ''' %\
                (profile_name, profile_name)
        cur.execute(query)
        conn.commit()
        rows=cur.rowcount
        if cur.rowcount == 0:
            query = '''insert into profile_names values ('%s')''' % (profile_name)
            cur.execute(query)
            conn.commit()
            # print ("inserted")
        else:
            # print ("updated")
            pass
    except sqlite3.OperationalError as e:
        print ("SQL read error: " + str(e))

    cur.execute('''select rowid from profile_names WHERE name='%s' ''' % profile_name)
    allentries = cur.fetchall()
    return(allentries[-1]['rowid'])
# }}}
def store_profile_in_db(db_file, profile_name):# {{{
    temps ={'t_lo': 't_lo', 't_med':  't_med', 't_high':  't_high', 't_hottt':  't_hottt'}
    profile = profile_generator(profile_name, 'tmp', temps)
    profile_id = get_profile_id_by_name(db_file, profile_name)

    print (json.dumps(profile, sort_keys=False, indent=4, separators=(',', ': ')))
    for i in range (1, 14):
        try:
            # Setup SQL connection # {{{
            conn = sqlite3.connect(db_file)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            # }}}
            query = '''update profiles set profile_id=%d, number=%d, temp='%s', time=%d '''\
                    '''WHERE profile_id=%d AND number=%d ''' %\
                    (profile_id, i,
                     profile['TEMPERATURE_WEEKDAY_%d'%i], profile['ENDTIME_WEEKDAY_%d'%i],
                     profile_id, i)
            cur.execute(query)
            conn.commit()
            rows=cur.rowcount
            if cur.rowcount == 0:
                query = '''insert into profiles values (%d, %d, '%s', %d) ''' %\
                        (profile_id, i,
                         profile['TEMPERATURE_WEEKDAY_%d'%i], profile['ENDTIME_WEEKDAY_%d'%i])
                cur.execute(query)
                conn.commit()
                # print ("insert")
            # else:
                # print ("update")
        except sqlite3.OperationalError as e:
            print ("SQL read error: " + str(e))
    conn.close()
# }}}
def get_profile_from_db(db_file, profile_name):# {{{
    profile_id = get_profile_id_by_name(db_file, profile_name)

    for i in range (1, 14):
        try:
            # Setup SQL connection # {{{
            conn = sqlite3.connect(db_file)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            # }}}
            query = '''select * from profiles WHERE profile_id=%d ''' % (profile_id)
            cur.execute(query)
            conn.commit()
            allentries = cur.fetchall()
        except sqlite3.OperationalError as e:
            print ("SQL read error: " + str(e))
    conn.close()
    return(allentries)
# }}}
################### /sqlite ##############

################## MAIN ########################
(args, parser) = parseOptions()
if dry_run:
    args.verbose += 1

# Setup logging{{{
# logformat = "{%(asctime)s %(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s"
logformat = "%(asctime)s %(funcName)s:%(lineno)d} %(levelname)s - %(message)s"
loglevel = logging.getLevelName(args.loglevel.upper())
logging.basicConfig(level=loglevel, format=logformat, filename=args.logfile)
# logging.debug('homematirc_profiler- v.0.0.3')
# }}}
logging.info(' '.join(sys.argv))
init_sqlite_tables(args.db_file)

if args.put_t: # put a temperature value # {{{
    # one of the values must me nonzero
    values_to_set = []
    temps = {}
    temps['t_lo']    = args.t_lo
    temps['t_med']   = args.t_med
    temps['t_high']  = args.t_high
    temps['t_hottt'] = args.t_hottt
    for value in ['t_lo', 't_med', 't_high', 't_hottt']:
        if temps[value] != 0:
            values_to_set.append(value)
    if values_to_set == []:
        print ("No nonzero temperature provided; Fatal!")
        exit (3)
    print ('Setting %s' % str(values_to_set))

    try:
        temps = read_temps_entry_from_db(args.db_file, args.device)
        print ("sql read successful")
        print (json.dumps(temps, sort_keys=False, indent=4, separators=(',', ': ')))
        for value in values_to_set:
            temps[value] = getattr(args, value)
            print("setting: %s %f" % (value, getattr(args, value)))
    except Exception as e:
        print  ("Except: %s" % str(e))
        raise

    store_temps_entry_in_db(args.db_file, args.device, temps)

    exit (0)
# }}}
if args.put_all:# {{{
    # sanity checking:
    if args.device is None:
        print("device is not specified but required when using --put")
        exit(2)
    temps        = read_temps_entry_from_db(args.db_file, args.device)
    for day in weekdays:
        profile_name = read_profile_entry_from_db(args.db_file, args.device, day)
        profile      = profile_generator(profile_name, day, temps)
        if args.verbose > 1:
            print (json.dumps(profile, sort_keys=False, indent=4, separators=(',', ': ')))
        if not dry_run:
            hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
            hg.putParamset(args.device, 0, "MASTER", profile)
            logging.info('sending profile %s for %s to homegear device %d' % (profile_name, day, args.device))
        if args.verbose:
            logging.info('sending profile %s for %s to homegear device %d ' % (profile_name, day, args.device))
# }}}
if args.put:# profile # {{{
    # sanity checking:
    if args.device is None:
        print("device is not specified but required when using --put")
        exit(2)

    if args.day is None:
        print("day is not specified but required when using --put")
        exit(0)

    if args.profile_name is None:
        print("day is specified, but profile_name not. This is required when using --put and --day")
        exit(1)

    store_profile_entry_in_db(args.db_file, args.device, args.day, args.profile_name)

    ### TODO: This stuff could go to "args.store or args.transfer"
    temps        = read_temps_entry_from_db(args.db_file, args.device)
    profile = profile_generator(args.profile_name, args.day, temps)
    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
        hg.putParamset(args.device, 0, "MASTER", profile)
        logging.info('sending profile %s for %s to homegear' % (args.profile_name, args.day))
    print (args.profile_name)
# }}}
if args.get: # {{{
    profile_name = read_profile_entry_from_db(args.db_file, args.device, args.day)
    temps        = read_temps_entry_from_db(args.db_file, args.device)
    print (profile_name)

    profile = profile_generator(profile_name, args.day, temps)

    if args.verbose:
        print (json.dumps(profile, sort_keys=False, indent=4, separators=(',', ': ')))
# }}}
if args.get_t: # {{{
    # sanity checking:
    if args.device is None:
        print("device is not specified but required when using --put")
        exit(6)

    temps = read_temps_entry_from_db(args.db_file, args.device)
    print (str(temps))
# }}}
if args.get_all: # {{{
    temps = read_temps_entry_from_db(args.db_file, args.device)
    for day in weekdays:
        temps[day] = read_profile_entry_from_db(args.db_file, args.device, day)
    print (str(temps))
# }}}
if args.device_get_t:# {{{
    # sanity checking:

    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
        # device_profile = hg.getParamset(args.device, 0, "MASTER")
        device_profile = hg.getAllConfig()
        print (json.dumps(device_profile, sort_keys=True, indent=4, separators=(',', ': ')))
# }}}


if args.pull_from_device: # {{{
    # sanity checking:
    if args.device is None:
        print("device is not specified but required")
        exit(6)

    # get profile for device from device
    dev_profile={}
    if not dry_run:
        hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
        device_profile = hg.getParamset(args.device, 0, "MASTER")
        logging.info('got profile for %d from homegear' % (args.device))
        for day in weekdays:
            dev_profile[day]={}
            day_name = days[day]
            for num in range (1, 14):
                dev_profile[day]["TEMPERATURE_%s_%d"%(day_name, num)] = device_profile["TEMPERATURE_%s_%d"%(day_name, num)]
                dev_profile[day]["ENDTIME_%s_%d"%(day_name, num)]     = device_profile["ENDTIME_%s_%d"%(day_name, num)]
        # print (json.dumps(dev_profile, sort_keys=False, indent=4, separators=(',', ': ')))

    # get profile for device from database
    db_profile={}
    for day in weekdays:
        db_profile_name = read_profile_entry_from_db(args.db_file, args.device, day)
        temps           = read_temps_entry_from_db(args.db_file, args.device)
        db_profile[day] = profile_generator(db_profile_name, day, temps)
    # print (json.dumps(db_profile, sort_keys=False, indent=4, separators=(',', ': ')))

    for day in weekdays:
        day_name = days[day]
        for num in range (1, 14):
            # print (json.dumps(dev_profile, sort_keys=False, indent=4, separators=(',', ': ')))
            # print (json.dumps(db_profile, sort_keys=False, indent=4, separators=(',', ': ')))
            diff_temp = dev_profile[day]["TEMPERATURE_%s_%d"%(day_name, num)] - \
                         db_profile[day]["TEMPERATURE_%s_%d"%(day_name, num)]
            diff_time = dev_profile[day]["ENDTIME_%s_%d"%(day_name, num)] - \
                         db_profile[day]["ENDTIME_%s_%d"%(day_name, num)]
            if diff_temp != 0 or diff_time !=0:
                temp_a = dev_profile[day]["TEMPERATURE_%s_%d"%(day_name, num)]
                temp_b =  db_profile[day]["TEMPERATURE_%s_%d"%(day_name, num)]
                time_a = dev_profile[day]["ENDTIME_%s_%d"%(day_name, num)]
                time_b =  db_profile[day]["ENDTIME_%s_%d"%(day_name, num)]
                print ('%(day)s: Different values in step %(num)d:\n'\
                        '    TEMP: %(temp_a)d != %(temp_b)d\n'\
                        '    TIME: %(time_a)d != %(time_b)d' % locals())
            # else:
                # tempa = dev_profile[day]["TEMPERATURE_%s_%d"%(day_name, num)]
                # tempb =  db_profile[day]["TEMPERATURE_%s_%d"%(day_name, num)]
                # timea = dev_profile[day]["ENDTIME_%s_%d"%(day_name, num)]
                # timeb =  db_profile[day]["ENDTIME_%s_%d"%(day_name, num)]
                # print ('%(day)s: Same values in step %(num)d:\n'\
                #         '    TEMP: %(tempa)d != %(tempb)d\n'\
                #         '    TIME: %(timea)d != %(timeb)d' % locals())


# }}}
if args.create_profile is not None:
    profile_name = args.create_profile
    store_profile_in_db(args.db_file, profile_name)
    # }}}
if args.create_all_profiles is not None:
    for profile_name in allowed_profile_names:
        store_profile_in_db(args.db_file, profile_name)
    # }}}
if args.get_profile is not None:
    profile_name = args.get_profile
    raw_profile = get_profile_from_db(args.db_file, profile_name)
    profile=[]
    for p in raw_profile:
        profile.append({})
        profile[-1]['number'] = p['number']
        profile[-1]['temp']   = p['temp']
        profile[-1]['time']   = p['time']
    print (json.dumps(profile, sort_keys=False, indent=4, separators=(',', ': ')))
