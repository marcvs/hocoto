#!/usr/bin/env python3
'''test'''
# pylint # {{{
# vim: tw=100 foldmethod=marker
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# }}}


import sys
import os
import datetime
import json
import logging
import configargparse
from homegear import Homegear

def parseOptions():# {{{
    '''Parse the commandline options'''

    path_of_executable = os.path.realpath(sys.argv[0])
    folder_of_executable = os.path.split(path_of_executable)[0]

    config_files = [os.environ['HOME']+'/.config/ldf-interface.conf',
                    folder_of_executable + '/ldf-interface.conf',
                    '/root/configs/ldf-interface.conf']

    parser = configargparse.ArgumentParser(
            default_config_files = config_files,
            description='''test''')
    parser.add('-c', '--my-config', is_config_file=True, help='config file path')
    parser.add_argument('--verbose', '-v', action="count", default=0, help='Verbosity')
    parser.add_argument('all_args', nargs='*')
    parser.add_argument('--logfile', default='/tmp/test-py.log')
    parser.add_argument('--loglevel',                      default='debug')
    parser.add_argument('--device', type=int)
    parser.add_argument('--day', choices = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
    parser.add_argument('--mode', choices = ["fma", "ma", "t", "ta", "a"])

    args = parser.parse_args()
    print(parser.format_values())
    return args, parser
#}}}

def eventHandler(eventSource, peerId, channel, variableName, value):
    # This callback method is called on Homegear variable changes
    '''event handler'''
    # Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
    # needed when you access non local variables.
    print("Event handler called with arguments: source: " + eventSource + \
            ";\n     peerId: " + str(peerId) + \
            ";\n     channel: " + str(channel) + \
            ";\n     variable name: " + variableName + \
            ";\n     value: " + str(value))

# Global variables
now = datetime.datetime.now()
days = {'mon': 'MONDAY',
        'tue': 'TUESDAY',
        'wed': 'WEDNESDAY',
        'thu': 'THURSDAY',
        'fri': 'FRIDAY',
        'sat': 'SATURDAY',
        'sun': 'SUNDAY',
        'today': now.strftime("%A").upper() }

params={}

params["TEMPERATURE_MONDAY_2"]= 13
params["TEMPERATURE_MONDAY_3"]= 12

day = "TEMPERATURE_MONDAY_4"
temp= 11
params[day] = temp

day_num = 5
day_name = "MONDAY"

params["TEMPERATURE_%s_%d"%(day_name, day_num)] = 10

profiles={}
profiles['fma'] = params
profiles['ma'] = params

print ('params:')
print (json.dumps(params, sort_keys=True, indent=4, separators=(',', ': ')))

print ('profiles:')
print (json.dumps(profiles, sort_keys=True, indent=4, separators=(',', ': ')))


print ("Type: %s" % type(days))
print ("day: %s" % days['tue'])
print ("day: %s" % days['today'])
exit(0)




(args, parser) = parseOptions()

logformat = "{%(asctime)s %(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s"
loglevel = logging.getLevelName(args.loglevel.upper())
logging.basicConfig(level=loglevel, format=logformat, filename=args.logfile)
logging.debug('\n\n\ntest- v.0.0.1')

logging.info(parser.format_values())

# input_data = sys.stdin.read()
# logging.info(input_data)



# | ID | Name                      | Address | Serial     | Type | Type String |
# |----+---------------------------+---------+------------+------+-------------|
# | 1  | HM Entkleide OEQ1718409   | 63A25E  | OEQ1718409 | 095 | HM-CC-RT-DN |
# | 2  | HM Wohnzimmer OEQ1711775  | 638586  | OEQ1711775 | 095 | HM-CC-RT-DN |
# | 3  | HM Kueche vorn OEQ1711363 | 638718  | OEQ1711363 | 095 | HM-CC-RT-DN |
# | 4  | HM Kueche hinten  OEQ1... | 63A260  | OEQ1718411 | 095 | HM-CC-RT-DN |
# | 5  | HM Gaestezimmer OEQ171... | 63A278  | OEQ1718437 | 095 | HM-CC-RT-DN |
# | 6  | HM Bad OEQ1718406         | 63A255  | OEQ1718406 | 095 | HM-CC-RT-DN |
hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)

# in_params = hg.getParamset(1, 0, "MASTER")


# setattr(params, "TEMPERATURE_MONDAY_4", 11)
# print (str(params))

# hg.putParamset(1,0, "MASTER", params)

