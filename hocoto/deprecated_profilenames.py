#!/usr/bin/env python3
'''parse commanline arguments'''
# pylint
# vim: tw=100 
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements

allowed_profile_names = ["fma", "ma", "t", "ta", "a", "o"]
default_t_lo          = 17.0
default_t_med         = 19.0
default_t_high        = 20.0
default_t_hottt       = 21.0
