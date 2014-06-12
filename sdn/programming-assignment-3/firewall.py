'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv
from itertools import islice

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

class Firewall (EventMixin):
    rules = []

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

        f = open(policyFile)
        try:
            reader = csv.reader(f)
            for row in islice(reader, 1, None):
                print "Firewall rule:", row
                self.rules.append({'src':row[1], 'dst':row[2]});
        finally:
            f.close()

    def _handle_ConnectionUp (self, event):
        for i,rule in enumerate(self.rules):
            dropmsg = of.ofp_flow_mod()
            dropmsg.priority = i + 100
            dropmsg.match = of.ofp_match(dl_src = EthAddr(rule['src']), dl_dst = EthAddr(rule['dst']))
            event.connection.send(dropmsg)
            log.info("Adding a drop rule for link %s -> %s", rule['src'], rule['dst'])

        msg = of.ofp_flow_mod()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        msg.priority = 1
        event.connection.send(msg)
        log.info("Hubifying %s", dpidToStr(event.dpid))

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
