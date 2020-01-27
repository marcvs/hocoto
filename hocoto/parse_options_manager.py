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
    parser.add_argument('--debug',   '-x',       action='store_true',     default=False)
    parser.add_argument('--device',  '-d',       default=False)
    parser.add_argument('--plot',    '-p',       action='store_true',     default=False)
    parser.add_argument('--plot_dedup',  '-pd',  action='store_true',     default=False)
    parser.add_argument('--dump',                action='store_true',     default=False)
    parser.add_argument('--table',   '-t',       action='store_true',     default=False)
    parser.add_argument('--table-dedup', '-td',  action='store_true',     default=False)
    parser.add_argument('--day',                 type=str, default=None)
    parser.add_argument('--daynum')
    parser.add_argument('--copy',    '-c',       action='store_true',     default=False)
    parser.add_argument('--todev',               default=False)
    parser.add_argument('--fromday',             type=str, default=None)
    parser.add_argument('--today',               choices = weekdays)
    parser.add_argument('--width',               type=int, default=40)
    parser.add_argument('--max_devices',         type=int, default=10)
    parser.add_argument('--list',  '-l',         action='store_true',     default=False)
    parser.add_argument('--readfromfile', '-r',  default = None)
    parser.add_argument('--writetofile',  '-w',  default = None)
    parser.add_argument('--inn', '--in', '-in',  default = None, help='''<type>:<value>', with
            type_spec in 'file', 'dev', 'device' and value either a file name or a device name''')
    parser.add_argument('--out', '-o', '-out',   default = None, help='''<type>:<value>', with
            type_spec in 'file', 'dev', 'device' and value either a file name or a device name''')

    # args = parser.parse_args()
    # print(parser.format_values())
    # return args, parser
    return parser

# reparse args on import
args = parseOptions().parse_args()

# pre process arguments:
if args.day:
        args.day = args.day.upper()
if args.today:
        args.today = args.today.upper()
if args.fromday:
        args.fromday = args.fromday.upper()

# overwrite a couple of values, for the sake of a simplified usage:
if args.inn:
    if len(args.inn.split(":")) != 2:
        print (F"Parameter --in malformed. Must be of form '<type>:<value>', was: {args.inn}")
        exit (6)
    try:
        (type_spec, param_value) = args.inn.split(':')
    except Exception as e:
        print (F"Error: {e}")
        raise
    if type_spec in ('file'):
        args.readfromfile = param_value
    if type_spec in ('dev', 'device'):
        args.device = param_value

if args.out:
    if len(args.out.split(":")) != 2:
        print (F"Parameter --out malformed. Must be of form '<type>:<value>', was: {args.out}")
        exit (7)
    try:
        (type_spec, param_value) = args.out.split(':')
    except Exception as e:
        print (F"Error: {e}")
        raise
    if type_spec in ('file'):
        args.writetofile = param_value
    if type_spec in ('dev', 'device'):
        args.todev = param_value
