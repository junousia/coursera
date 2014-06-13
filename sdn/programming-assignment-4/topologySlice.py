'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()

rules = {
    "00-00-00-00-00-01":[ {'in_port':3, 'out_port':1}, {'in_port':2, 'out_port':4}, {'in_port':1, 'out_port':3}, {'in_port':4, 'out_port':2}],
    "00-00-00-00-00-02":[ {'in_port':1, 'out_port':2}, {'in_port':2, 'out_port':1} ],
    "00-00-00-00-00-03":[ {'in_port':1, 'out_port':2}, {'in_port':2, 'out_port':1} ],
    "00-00-00-00-00-04":[ {'in_port':3, 'out_port':1}, {'in_port':2, 'out_port':4}, {'in_port':1, 'out_port':3}, {'in_port':4, 'out_port':2}]
    }


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")

    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):

        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)

        for rule in rules[dpid]:
            log.debug("Installing forwarding rule on %s: in_port: %d -> out_port: %d", dpid, rule['in_port'], rule['out_port'])
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match(in_port = rule['in_port'])
            msg.actions.append(of.ofp_action_output(port = rule['out_port']))
            event.connection.send(msg)


def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
