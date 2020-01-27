#!/usr/bin/env python3
'''homematic day profile'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements
import fileinput
import logging
import re
from hocoto.parse_options_manager import args
from hocoto.homematic_day_profile import HomematicDayProfile
from hocoto.weekdays import weekdays, daynames, shortnames

logger = logging.getLogger(__name__)

def ensure_is_list(item):
    '''Make sure we have a list'''
    if isinstance(item, str):
        return [item]
    return item

class HomematicProfile():
    '''Class to capture homematic profiles'''
    def __init__(self, profile=None, days=None):
        '''init'''
        self.hm_day_profiles = {}
        if profile is not None:
            self.set_profile(profile, days)
    def set_profile(self, profile, days=None):
        '''add profile to class instance'''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays

        for day in days:
            self.hm_day_profiles[day] = HomematicDayProfile()
            # self.profile_dict[day]={}
            # self.profile_dict[day]['temp']=[]
            # self.profile_dict[day]['time']=[]
            day_name = daynames[day]
            for num in range (1, 14):
                # profile_dict[day][temp][num] = profile["TEMPERATURE_%s_%d"%(day_name, num)]
                # profile_dict[day][time][num] = profile["ENDTIME_%s_%d"%(day_name, num)]
                self.hm_day_profiles[day].add_step(profile["TEMPERATURE_%s_%d"%(day_name, num)],
                                                   profile["ENDTIME_%s_%d"%(day_name, num)])
    def get_profile(self, days=None):
        '''Get homematic profile for given weekday(s)'''
        output_dict = {}
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            if not self.profile_dict[day]:
                continue
            day_name = daynames[day]
            for num in range (1, 14):
                # output_dict["TEMPERATURE_%s_%d"%(day_name, num)] = self.profile_dict[day]['temp'][num]
                # output_dict["ENDTIME_%s_%d"%(day_name, num)]     = self.profile_dict[day]['time'][num]
                (time, temp) = self.hm_day_profiles[day].get_step(num)
                output_dict["ENDTIME_%s_%d"%(day_name, num)]     = time
                output_dict["TEMPERATURE_%s_%d"%(day_name, num)] = temp
    def __repr_table__(self, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            rv += F"{daynames[day]}\n"
            rv += self.hm_day_profiles[day].__repr_table__()
        return rv
    def __repr_table_dedup__(self, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            day_num = weekdays.index(day)
            dupe_found = False
            dupe_name = ""
            for prev_day_num in range (0,day_num):
                prev_day = weekdays[prev_day_num]
                if self.hm_day_profiles[day] == self.hm_day_profiles[prev_day]:
                    dupe_found = True
                    dupe_name  = prev_day
                    break
            rv += (F"{daynames[day]}\n")
            if not dupe_found:
                rv += self.hm_day_profiles[day].__repr_table__()
            else:
                rv += F"Same as {daynames[dupe_name]:.7}\n"
        return rv
    def __repr_tables_multi__(self):
        rv = ''
        plots = {}
        lines = {}
        # convert plots to lines
        for day in weekdays:
            plots[day] = self.__repr_table_dedup__(days=day)
            lines[day] = plots[day].split('\n')

        maxlines = 0
        for day in weekdays:
            if len(lines[day]) > maxlines:
                maxlines = len(lines[day]) 

        for i in range (0, maxlines-1):
            for day in weekdays:
                try:
                    entry = lines[day][i].rstrip('\n')
                    rv += F"{entry:<15}| "
                except IndexError:
                    rv += "{:<15}| ".format(" ")

            rv += "\n"
        return rv
    def __repr_table_dedup_all__(self, days=None):
        '''Table view of the profile'''
        rv = ''
        alldays=[]
        for day in self.hm_day_profiles:
            alldays.append(day)
            # print (F"aaaaaaaaaaaaaaaaaaa> {day}")
            try:
                daynames[day]
            except KeyError:
                daynames[day] = day
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in alldays:
            # day_num = weekdays.index(day)
            day_num = alldays.index(day)
            dupe_found = False
            dupe_name = ""
            for prev_day_num in range (0,day_num):
                prev_day = alldays[prev_day_num]
                if self.hm_day_profiles[day] == self.hm_day_profiles[prev_day]:
                    dupe_found = True
                    dupe_name  = prev_day
                    break
            rv += (F"{daynames[day]}\n")
            if not dupe_found:
                rv += self.hm_day_profiles[day].__repr_table__()
            else:
                rv += F"Same as {daynames[dupe_name]:<7}\n"
        return rv
    def __repr_plot__(self, width=40, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            try:
                rv += F"{daynames[day]}\n"
            except KeyError:
                pass
            try:
                rv += self.hm_day_profiles[day].__repr_plot__(width = width)
            except KeyError:
                rv += F'No Profile for "{day}"'
        return rv
    def __repr_plot_dedup__(self, width=40, days=None):
        '''Table view of the profile'''
        rv = ''
        if days is not None:
            days = ensure_is_list (days)
        else:
            days = weekdays
        for day in days:
            day_num = weekdays.index(day)
            dupe_found = False
            dupe_name = ""

            for prev_day_num in range (0,day_num):
                prev_day = weekdays[prev_day_num]
                if self.hm_day_profiles[day] == self.hm_day_profiles[prev_day]:
                    dupe_found = True
                    dupe_name  = daynames[prev_day]
                    break
            rv += (F"{daynames[day]}\n")
            if not dupe_found:
                rv += self.hm_day_profiles[day].__repr_plot__(width = width)
            else:
                def string_insert (source_str, insert_str, pos):
                    return source_str[:pos]+insert_str+source_str[pos:]
                def string_ins_replace (source_str, insert_str, pos):
                    length = len(insert_str)
                    return source_str[:pos]+insert_str+source_str[pos+length:]
                tmp = self.hm_day_profiles[day].__repr_plot__(width = width)
                tmplines = tmp.split('\n')
                linewidth = len(tmplines[1]) -2
                # tmplines[2]=string_ins_replace(tmplines[2], "+------------+",  8)
                # tmplines[3]=string_ins_replace(tmplines[3], "|            | ", 8)
                # tmplines[4]=string_ins_replace(tmplines[4], "|  same as   | ", 8)
                # tmplines[5]=string_ins_replace(tmplines[5], "|  {: <10}|".format(dupe_name), 8)
                # tmplines[6]=string_ins_replace(tmplines[6], "|            | ", 8)
                # tmplines[7]=string_ins_replace(tmplines[7], "+------------+ ", 8)
                tmplines[0]= ("+{:-^%d}+"%linewidth).format("-")
                tmplines[1]= ("+{: ^%d}+"%linewidth).format(" ")
                tmplines[2]= ("|{: ^%d}|"%linewidth).format("same as")
                tmplines[3]= ("|{: ^%d}|"%linewidth).format(dupe_name)
                tmplines[4]= ("+{: ^%d}+"%linewidth).format(" ")
                tmplines[5]= ("+{:-^%d}+"%linewidth).format("-")
                tmp = "\n".join (tmplines)
                rv += tmp

        return rv
    def __repr_plots_multi__(self, width, plots_per_row=3):
        '''mutliple plots in a row'''
        plots = {}
        lines = {}
        do_summary = False
        if plots_per_row == 3:
            do_summary = True
        plots_per_row  -= 1
        blocks_to_plot = int (7 / plots_per_row - 0.1)+1
        rv = ''

        # convert plots to lines
        for day in weekdays:
            plots[day] = self.__repr_plot_dedup__(width, days=day)
            lines[day] = plots[day].split('\n')

        linewidth = len(lines[day][1]) 

        for blocks in range (0, blocks_to_plot*plots_per_row, plots_per_row+1):
            for i in range (blocks, blocks + plots_per_row + 1):
                try:
                    rv += (("{:^%d}  " % linewidth).format(daynames[weekdays[i]]) )
                except IndexError:
                    pass
            rv += ('\n')
            for line in range (1, 16):
                for i in range (blocks, blocks + plots_per_row + 1):
                    if i < len(lines):
                        try:
                            rv += (F"{lines[weekdays[i]][line]}  ")
                        except IndexError:
                            pass
                rv += ("\n")
        return rv
    def __repr_dump__(self, day_in=None, day_out=None):
        if day_in is not None:
            return (self.hm_day_profiles[day_in].__repr_dump__(day_out))
        rv={}
        for day in weekdays:
            temp = self.hm_day_profiles[day].__repr_dump__(day)
            for entry in temp:
                rv[entry] = temp[entry]
                # print (F"  entry: {entry}")
        return rv
    def get_profilenames_from_file(self, filename):
        profile_names=[]
        for line in fileinput.input(filename):
            if line[0] == "#":
                continue
            elif re.match("[a-zA-Z]", line[0]):
                if line[:7] ==  "Same as":
                    continue
                elif "=" in line:
                    profile_names.append(line.split("=")[1].rstrip().lstrip())
                else:
                    profile_names.append(line.rstrip().lstrip())
        return profile_names
    def read_from_file(self, filename):
        current_profilename = None
        same_as = None
        for line in fileinput.input(filename):
            # print (F"LINE: {line}  [0]:>{line[0]}<")
            try:
                # if line[0] in "abcdefghijklmnopqrstuvwxyz":
                if line[0] == "#":
                    continue
                elif re.match("[a-zA-Z\=]", line[0]):
                    if line[:7] ==  "Same as":
                        same_as = line.split("Same as")[1].lstrip().rstrip().upper()
                        # print (F"                    >>{same_as}<<")
                    elif line[0] == "=":
                        same_as = line.split("=")[1].lstrip().rstrip().upper()
                        # print (F"           ======   >>{same_as}<<")
                    elif "=" in line:
                        name = line.split("=")[1].rstrip().lstrip().upper()
                    else:
                        name = line.rstrip().lstrip().upper()
                    if args.verbose:
                        print (F"\nProfilename: {name}")
                    current_profilename = name
                    if current_profilename in shortnames:
                            current_profilename = shortnames[current_profilename]
                    # if current_profilename.upper() in shortnames:
                    #         current_profilename = shortnames[current_profilename.upper()]
                elif line == "\n":
                    continue
                else:
                    (time, date) = line.split("-")
                    time = time.lstrip().rstrip()
                    (hrs, mins) = time.split(":")
                    minutes = 60*int(hrs) + int(mins)
                    temp = float(date.lstrip().rstrip().rstrip('C').rstrip('°'))
                    # print (F"Read: time: ({minutes}) {time} - temp: {temp}")
                    if not current_profilename in self.hm_day_profiles.keys():
                        self.hm_day_profiles[current_profilename] = HomematicDayProfile()
                    self.hm_day_profiles[current_profilename].add_step(temp, minutes)
                    # print (F"storing for profile {current_profilename}")
                    # if current_profilename == profilename:
                    #     self.add_step(temp, minutes)
                if same_as:
                    # print (F"     -------------- >>{same_as}<<")
                    if same_as.upper() in shortnames:
                            same_as = shortnames[same_as.upper()]
                    self.hm_day_profiles[current_profilename] = self.hm_day_profiles[same_as]
                    same_as = None
            except ValueError as e:
                # pass
                print (F"exception: {e}\nline: '{line}'")
                if args.debug:
                    raise
        # print ("Listing all profiles read")
        # make sure each profile is complete:
        for p in self.hm_day_profiles:
            for step in range (self.hm_day_profiles[p].steps_stored, 14):
                # print (F"missing step: {step}")
                self.hm_day_profiles[p].add_step(self.hm_day_profiles[p].temp[-1], 1440)
        #     print (p)
        # print ("done")
        # import json
        # print (json.dumps(self.hm_day_profiles, sort_keys=False, indent=4, separators=(',', ': ')))
        # print (self.__repr_table__())

