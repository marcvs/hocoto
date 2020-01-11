#!/usr/bin/env python3
'''homematic event handler'''
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# pylint: disable=multiple-statements

def eventHandler(eventSource, peerId, channel, variableName, value):
    # This callback method is called on Homegear variable changes
    # Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
    # needed when you access non local variables.

    # print("Event handler called with arguments: source: " + eventSource + \
    #         ";\n     peerId: " + str(peerId) + \
    #         ";\n     channel: " + str(channel) + \
    #         ";\n     variable name: " + variableName + \
    #         ";\n     value: " + str(value))
    pass
