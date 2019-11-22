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
    parser.add_argument('--device',        type=int, default=1)

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

# hg.setSystemVariable("TEST", 6)
# print(hg.getSystemVariable("TEST"))


# print_v($hg->getParamset($device, 0, "MASTER"));
# print(hg.getParamset(1, 0, "MASTER"))

MODES=[ 'AUTO-MODE' ,'MANU-MODE' ,'PARTY-MODE' ,'BOOST-MODE']

device = args.device
print("\nDevice %d" % device)
print(hg.getValue(device, 4, "CONTROL_MODE"))
print(hg.getValue(device, 4, "SET_TEMPERATURE"))

print(hg.setValue(device, 4, "MANU_MODE", True))
print(hg.setValue(device, 4, "SET_TEMPERATURE", 16.5))

print(hg.getValue(device, 4, "SET_TEMPERATURE"))
print(hg.getValue(device, 4, "CONTROL_MODE"))

# print(hg.getParamset(device, 4, "MASTER"))
data = hg.getAllValues(device)

import json
print (json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))

print("done")
