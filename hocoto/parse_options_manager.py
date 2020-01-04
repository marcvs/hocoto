#!/usr/bin/env python3
'''parse commandline options'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements

import sys
import os
import configargparse
import logging
from hocoto.weekdays import weekdays, days

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
    parser.add('--my-config', is_config_file=True, help='config file path')
    parser.add_argument('--verbose', '-v',       action="count", default=0, help='Verbosity')
    parser.add_argument('--device',  '-d',       type=int)
    parser.add_argument('--plot',    '-p',       action='store_true',     default=False)
    parser.add_argument('--dump',                action='store_true',     default=False)
    parser.add_argument('--table',   '-t',       action='store_true',     default=False)
    parser.add_argument('--day',                 choices = weekdays)
    parser.add_argument('--daynum')
    # parser.add_argument('--day',                 choices = weekdays)
    parser.add_argument('--copy',    '-c',       action='store_true',     default=False)
    parser.add_argument('--todev',               type=int, default=0)
    parser.add_argument('--fromday',             choices = weekdays)
    parser.add_argument('--today',               choices = weekdays)
    parser.add_argument('--width',        '-w',  type=int, default=40)
    parser.add_argument('--readfromfile', '-r',  default = None)
    parser.add_argument('--profilename',  '-n',  default = None)
    parser.add_argument('--writetofile',  '-f',  default = None)

    # args = parser.parse_args()
    # print(parser.format_values())
    # return args, parser
    return parser

# reparse args on import
args = parseOptions().parse_args()
