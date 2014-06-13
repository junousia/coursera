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

from itertools import permutations
from itertools import cycle

log = core.getLogger()


class VideoSlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        core.openflow_discovery.addListeners(self)

        # Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
        self.adjacency = defaultdict(lambda:defaultdict(lambda:None))

        '''
        The structure of self.portmap is a four-tuple key and a string value.
        The type is:
        (dpid string, src MAC addr, dst MAC addr, port (int)) -> dpid of next switch
        '''

        self.portmap = { }

        self.linkmap = {
                '00-00-00-00-00-01': {
                    'video':{'left':[4,3],'right':[2]},
                    'any':{'left':[4,3],'right':[1]}
                    },
                '00-00-00-00-00-02': {
                    'video':{'left':[1],'right':[2]},
                    'any':{'left':[1],'right':[2]}
                    },
                '00-00-00-00-00-03': {
                    'video':{'left':[1],'right':[2]},
                    'any':{'left':[1],'right':[2]}
                    },
                '00-00-00-00-00-04': {
                    'video':{'left':[2],'right':[4,3]},
                    'any':{'left':[1],'right':[4,3]},
                }
        }

        switches = ['00-00-00-00-00-01', '00-00-00-00-00-02', '00-00-00-00-00-03', '00-00-00-00-00-04']

        lhosts = [ '00:00:00:00:00:01', '00:00:00:00:00:02' ]
        rhosts = [ '00:00:00:00:00:03', '00:00:00:00:00:04' ]

        for switch in switches:
            log.debug("Configuring switch %s", switch)
            for src,dst in permutations(lhosts + rhosts, 2):
                if dst in lhosts:
                    videokey = (switch, EthAddr(src), EthAddr(dst), 80)
                    anykey = (switch, EthAddr(src), EthAddr(dst), 'any')
                    self.portmap[videokey] = self.linkmap[switch]['video']['left'][-(int(dst[-1]) % 2)]
                    self.portmap[anykey] = self.linkmap[switch]['any']['left'][-(int(dst[-1]) % 2)]
                    log.debug("Add key %s %s %s %s", switch, EthAddr(src),EthAddr(dst), self.linkmap[switch]['any']['left'][-(int(dst[-1]) % 2)])
                elif dst in rhosts:
                    videokey = (switch, EthAddr(src), EthAddr(dst), 80)
                    anykey = (switch, EthAddr(src), EthAddr(dst),'any')
                    log.debug("Add key %s %s %s %s", switch, EthAddr(src),EthAddr(dst), self.linkmap[switch]['any']['right'][-(int(dst[-1]) % 2)])
                    self.portmap[videokey] = self.linkmap[switch]['video']['right'][-(int(dst[-1]) % 2)]
                    self.portmap[anykey] = self.linkmap[switch]['any']['right'][-(int(dst[-1]) % 2)]

    def _handle_LinkEvent (self, event):
        l = event.link
        sw1 = dpid_to_str(l.dpid1)
        sw2 = dpid_to_str(l.dpid2)

        log.debug ("link %s[%d] <-> %s[%d]",
                   sw1, l.port1,
                   sw2, l.port2)

        self.adjacency[sw1][sw2] = l.port1
        self.adjacency[sw2][sw1] = l.port2


    def _handle_PacketIn (self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """
        packet = event.parsed
        tcpp = event.parsed.find('tcp')

        def install_fwdrule(event,packet,outport):
            msg = of.ofp_flow_mod()
            msg.idle_timeout = 10
            msg.hard_timeout = 30
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.actions.append(of.ofp_action_output(port = outport))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        def forward (message = None):
            this_dpid = dpid_to_str(event.dpid)

            if packet.dst.is_multicast:
                flood()
                return
            else:
                log.debug("Got unicast packet for %s at %s (input port %d):", packet.dst, dpid_to_str(event.dpid), event.port)
                try:
                    if tcpp.dstport != 80:
                        out_port = self.portmap[(this_dpid, packet.src, packet.dst, 'any')]
                    else:
                        out_port = self.portmap[(this_dpid, packet.src, packet.dst, 80)]

                    install_fwdrule(event, packet, out_port)

                except AttributeError:
                    log.debug("packet type has no transport ports, flooding")

                    # flood and install the flow table entry for the flood
                    install_fwdrule(event,packet,of.OFPP_FLOOD)

        # flood, but don't install the rule
        def flood (message = None):
            """ Floods the packet """
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        forward()


    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)


def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Video Slicing module
    '''
    core.registerNew(VideoSlice)
