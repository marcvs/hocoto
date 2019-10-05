#!/usr/bin/env python3

# pylint # {{{
# vim: tw=100 foldmethod=marker
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# }}}
import sys
import os
import configargparse
from homegear import Homegear

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
    parser.add_argument('--device','-d',   type=int, default=-1)
    parser.add_argument('--temp','-t',     type=float, default=-1)
    parser.add_argument('--mode','-m', 
        help="0:AUTO-MODE, 1:MANU-MODE,  2:PARTY-MODE, 3:BOOST-MODE",
        type=int, default=-1)

    args = parser.parse_args()
    # print(parser.format_values())
    return args, parser
#}}}

# This callback method is called on Homegear variable changes
def eventHandler(eventSource, peerId, channel, variableName, value):# {{{
	# Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
	# needed when you access non local variables.
	# print("Event handler called with arguments: source: " + eventSource + " peerId: " + str(peerId) + "; channel: " + str(channel) + "; variable name: " + variableName + "; value: " + str(value))
    pass
# }}}

(args, parser) = parseOptions()
hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)
MODES=[ 'AUTO_MODE' ,'MANU_MODE' ,'PARTY_MODE' ,'BOOST_MODE']

print (" Desired mode: {}".format(MODES[args.mode]))

if (args.device != -1):
    devices = [args.device]
else:
    devices = range (1, 7)
print ("+-------+-----+-----------------+------------+------+")
print ("| State | Dev#|  Name           |  Mode      | Temp |")
print ("+-------+-----+-----------------+------------+------+")
for device in devices:
    mode = hg.getValue(device, 4, "CONTROL_MODE")
    temp = hg.getValue(device, 4, "SET_TEMPERATURE")
    name = hg.getName(device)
    print("| Curr  | {: ^3} | {: <15} | {: <10} | {: <4} |".format(device, name, MODES[mode], temp))

    if (args.mode != -1 or (args.temp != -1 and temp != args.temp)):
        hg.setValue(device, 4, MODES[args.mode], True)
        hg.setValue(device, 4, "SET_TEMPERATURE", args.temp)

        mode = hg.getValue(device, 4, "CONTROL_MODE")
        temp = hg.getValue(device, 4, "SET_TEMPERATURE")
        print("| New   | {: ^3} | {: <15} | {: <10} | {: <4} |".format(device, name, MODES[mode], temp))
        if device != devices[-1]:
            print ("+.......+.....+.................+............+......+")

print ("+-------+-----+-----------------+------------+------+")

del(hg)
