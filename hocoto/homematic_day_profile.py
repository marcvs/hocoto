#!/usr/bin/env python3
'''homematic day profile'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements
import logging
from hocoto.weekdays import weekdays, days, daynames

logger = logging.getLogger(__name__)

class HomematicDayProfile():
    '''Class for just one day of homematic'''
    def __init__(self):
        self.profile_dict = {}
        self.time         = []
        self.temp         = []
        self.steps_stored = 0
    def add_step(self, temp, time):
        '''add one step to a profile'''
        if len(self.time) > 0:
            if self.time[-1] > time:
                print ("Timestep is lower than previous one. Closing profile.")
                self.time.append(1440)
                self.temp.append(self.temp[-1])
        self.time.append(time)
        self.temp.append(temp)
        # self.time[self.steps_stored] = time
        # self.temp[self.steps_stored] = temp
        self.steps_stored            += 1
    def read_from_file(self, filename, profilename = None):
        import fileinput
        current_profilename = None
        for line in fileinput.input(filename):
            try:
                # if line[0] in "abcdefghijklmnopqrstuvwxyz":
                if line[0] == "#":
                    continue
                elif line[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    if "=" in line:
                        name = line.split("=")[1].rstrip().lstrip()
                    else:
                        name = line.rstrip().lstrip()
                    if args.verbose:
                        print (F"\nProfilename: {name}")
                    current_profilename = name
                else:
                    (time, date) = line.split("-")
                    time = time.lstrip().rstrip()
                    (hrs, mins) = time.split(":")
                    minutes = 60*int(hrs) + int(mins)
                    temp = float(date.lstrip().rstrip().rstrip('C').rstrip('°'))
                    # print (F"Read: time: ({minutes}) {time} - temp: {temp}")
                    if current_profilename == profilename:
                        self.add_step(temp, minutes)
            except ValueError as e:
                pass
                # print (F"exception: {e}\nline: '{line}'")
        print (self.__repr_table__())
    def get_profile_step(self, step):
        '''get single timestep of a profile'''
        return (self.time[step], self.temp[step])
    def __repr_table__(self):
        rv=''
        try:
            for num in range(0, 14):
                total_minutes = self.time[num]
                hours = int(total_minutes / 60)
                minutes = total_minutes - hours*60
                # rv += (F"ENDTIME_{day_name}_{num:<2}: ")
                # rv += ("{}: ".format(num))
                rv += ("{:>2}:{:0<2}".format(hours,minutes))
                rv += (" - ")
                rv += ("{:<}°C\n".format( str(self.temp[num])))
                if total_minutes == 1440:
                    break
        except IndexError:
            pass # end of profile...

        return rv
    def __repr_plot__(self, width = 80):
        '''plot of the temperature graph'''
        rv=''
        time_divisor = int(80*20/width)
        n_time_axes = 180 # all xxx minutes
        if width < 40:
            n_time_axes = 360 # all xxx minutes
        residual = 0.99
        for temp_int in range(220,159,-5):
            cur_time_idx = 0
            temp = temp_int/10.0
            rv += ('{: <5}'.format(temp))

            rv += ('|')
            if (temp % 2 <= 0.1):
                rv += ('\b+')

            for time in range (1, int(1440/time_divisor)):
                dot_made = False
                if self.temp[cur_time_idx] == temp:
                    rv += ('*')
                    dot_made = True
                else:
                    rv += (' ')
                if self.time[cur_time_idx] < time*time_divisor:
                    cur_time_idx += 1
                if not dot_made:
                    if (time-1) % (60/time_divisor) <= residual:
                        rv += ('\b·')
                    if (time) % (n_time_axes/time_divisor) <= residual:
                        rv += ('\b|')
                    if (temp % 2 <= 0.1):
                        rv += ('\b-')
                    if (temp % 2 == 0) and ((time) % (n_time_axes/time_divisor) <= residual):
                        rv += ('\b+')
            rv += ('|')
            if (temp % 2 <= 0.1):
                rv += ('\b+')

            rv += ('\n')

        rv += ('      ')
        for time in range (1, int(1440/time_divisor)):
            hours = int(time*time_divisor/60)
            rv += (' ')
            if (time) % (n_time_axes/time_divisor) <= residual:
                rv += (F"\b\b{hours:>2}")
        rv += ("\b{:>2}".format(24))
        rv += ('\n')
        return rv
    # def __repr_dump__(self, day='mon'):
    def __repr_dump__(self, day=None):
        '''dump a homematic compatible dict for given day'''
        rv_dict={}
        dayname = ""
        if day is not None:
            dayname = daynames[day]
        for num in range(1, 14):
            rv_dict[F"ENDTIME_{dayname}_{num}"] = self.time[num-1]
            rv_dict[F"TEMPERATURE_{dayname}_{num}"] = self.temp[num-1]
        return rv_dict
    def __eq__(self, other):
        return self.__repr_dump__() == other.__repr_dump__()
