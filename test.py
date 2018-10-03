#!/usr/bin/env python3

# pylint # {{{
# vim: tw=100 foldmethod=marker
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy
# }}}
from homegear import Homegear

# This callback method is called on Homegear variable changes
def eventHandler(eventSource, peerId, channel, variableName, value):
	# Note that the event handler is called by a different thread than the main thread. I. e. thread synchronization is
	# needed when you access non local variables.
	print("Event handler called with arguments: source: " + eventSource + " peerId: " + str(peerId) + "; channel: " + str(channel) + "; variable name: " + variableName + "; value: " + str(value))

hg = Homegear("/var/run/homegear/homegearIPC.sock", eventHandler)

hg.setSystemVariable("TEST", 6)
print(hg.getSystemVariable("TEST"))


# print_v($hg->getParamset($device, 0, "MASTER"));
print(hg.getParamset(1, 0, "MASTER"))

print("done")
