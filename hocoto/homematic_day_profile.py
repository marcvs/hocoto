#!/usr/bin/env python3
'''homematic day profile'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements
import logging
import fileinput
import re
from hocoto.parse_options_manager import args
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
# Our data may look like this:
# self.temp: [16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 17.5, 17.5, 17.5, 17.5]
# self.time: [360,  361,  362,  363,  364,  485,  486,  487,  488,  489,  1440, 1440, 1440, 1440]

        residual = 0.9
        for temp_int in range(220,159,-5):
            temp          = temp_int/10.0
            hold_dot      = False
            time_next     = False
            previous_time = 0
            minidots_ctr  = 0
            # Y - Axis Numbers
            rv += ('{: <5}'.format(temp))
            # Y - Axis ticks
            if (temp % 2 <= 0.1):
                rv += ('+')
            else:
                rv += ('|')
            # X - Axis Loop (time)
            # for time in range (1, int(1440/time_divisor)):
            for time in range (1, 1440):
                # whether no make a plot decision
                if time % time_divisor <= residual:
                    make_dot = False
                    # Determine whether or not to make a dot for the given time / temp
                    for i in range (0,14):
                        try:
                            if self.time[i] > previous_time and self.time[i] <= time:
                                if self.temp[i] == temp:
                                    make_dot = True
                                # Hold the dot, until the next endtime entry:
                                if self.temp[i+1] == temp:
                                    hold_dot = True
                                else:
                                    hold_dot = False
                            else: # If we're before the first time step: Plt the first temperature
                                if time < self.time[0]:
                                    if self.temp[0] == temp:
                                        hold_dot = True
                        except IndexError:
                            pass
                    if hold_dot:
                        make_dot = True

                    if make_dot:
                        minidots_ctr += 1
                        rv += "*"
                    else:
                        minidots_ctr += 1
                        if (temp % 2 <= 0.1) and (time % n_time_axes < time_divisor):
                            rv += ('+')
                        # elif (time % n_time_axes) <= residual:
                        elif (time % n_time_axes) < time_divisor:
                            rv += ('|')
                        elif (temp % 2 <= 0.1):
                            rv += ('-')
                        else:
                            if minidots_ctr % 2 == 0:
                                rv += "·"
                            else:
                                rv += " "


                    # Loop end: store previous time
                    previous_time = time
            if temp in (22, 20, 18, 16):
                rv += "+\n"
            else:
                rv += "|\n"
        # X - Axis labels
        rv += ('       ')
        for time in range (1, 1440+1):
            if time % time_divisor <= residual:
                hours = int(time/60)
                if (time % n_time_axes) < time_divisor:
                    if hours > 9 and hours <= 12:
                        rv += "\b"
                    rv += (F"\b{hours:<2}")
                    # rv += ("{:>2}".format(24))
                    # rv += "I"
                else:
                    rv += " "
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
            try:
                rv_dict[F"ENDTIME_{dayname}_{num}"] = self.time[num-1]
                rv_dict[F"TEMPERATURE_{dayname}_{num}"] = self.temp[num-1]
            except IndexError:
                break
            except Exception as e:
                raise
        return rv_dict
    def __eq__(self, other):
        return self.__repr_dump__() == other.__repr_dump__()
