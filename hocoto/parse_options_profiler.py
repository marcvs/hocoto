#!/usr/bin/env python3
'''parse commandline arguments'''
# pylint
# vim: tw=100
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements

import sys
import os
import configargparse
import logging
from hocoto.weekdays import weekdays, days
from hocoto.deprecated_profilenames import allowed_profile_names

logger = logging.getLogger(__name__)

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

    # args = parser.parse_args()
    # print(parser.format_values())
    # return args, parser
    return parser

# reparse args on import
args = parseOptions().parse_args()
