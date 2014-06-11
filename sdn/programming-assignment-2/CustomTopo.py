'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections

from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        aggregation = []
        edge = []
        host = []

        self.linkopts = [ linkopts1, linkopts2, linkopts3 ]

        # Create core switch
        core = self.addSwitch('c1')

        # Aggregation switches
        for i in irange(1, fanout):
            aggregation.append(self.addSwitch('a%s' % (len(aggregation) + 1)))
            self.addLink(core, aggregation[-1], **linkopts1)

            # Edge switches
            for j in irange(1, fanout):
                edge.append(self.addSwitch('e%s' % (len(edge) + 1)))
                self.addLink(aggregation[-1], edge[-1], **linkopts2)

                # Hosts
                for k in irange(1, fanout):
                    host.append(self.addHost('h%s' % (len(host) + 1)))
                    self.addLink(host[-1], edge[-1], **linkopts3)

def main():
    """docstring for main"""

    "Create and test a simple network"
    topo = CustomTopo(
            {'bw':1, 'delay':'5ms', 'loss':0, 'max_queue_size':1000, 'use_htb':True},
            {'bw':1, 'delay':'5ms', 'loss':0, 'max_queue_size':1000, 'use_htb':True},
            {'bw':1, 'delay':'5ms', 'loss':0, 'max_queue_size':1000, 'use_htb':True}
            )
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

topos = { 'custom': ( lambda: CustomTopo() ) }
if __name__ == '__main__':
    setLogLevel('info')
    main()
