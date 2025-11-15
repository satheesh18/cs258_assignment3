from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink

class LinuxRouter(Node):
    def config(self, **params):
        super().config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super().terminate()

def add_route(node, subnet, via):
    node.cmd(f'ip route add {subnet} via {via}')

def run():
    net = Mininet(link=TCLink)

    print('Creating routers')
    r1 = net.addHost('r1', cls=LinuxRouter, ip='10.0.0.3/24')
    r2 = net.addHost('r2', cls=LinuxRouter, ip='10.0.1.2/24')

    print('Creating hosts')
    h1 = net.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.3')
    h2 = net.addHost('h2', ip='10.0.3.4/24', defaultRoute='via 10.0.3.2')
    h3 = net.addHost('h3', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1')

    print('Creating links')
    # Link from h1 to r1
    net.addLink(h1, r1, intfName2='r1-eth0', params2={'ip': '10.0.0.3/24'})

    # Route from r1 to r2 - for r1 to reach 10.0.2.0/24 (h3's subnet) via r2
    net.addLink(r1, r2,
                intfName1='r1-eth1', params1={'ip': '10.0.1.1/24'},
                intfName2='r2-eth0', params2={'ip': '10.0.1.2/24'})

    # Route from r2 to h3 - h3 is directly connected to r2
    net.addLink(r2, h3, intfName1='r2-eth1', params1={'ip': '10.0.2.1/24'})

    # Route from h2 to r1 - h2 is directly connected to r1
    net.addLink(h2, r1, intfName2='r1-eth2', params2={'ip': '10.0.3.2/24'})

    print('Starting network')
    net.start()

    print('Configuring routing tables')

    # r1: to reach h3 network, go to r2
    add_route(r1, '10.0.2.0/24', '10.0.1.2')

    # r2: to reach h1 and h2 networks, go to r1
    add_route(r2, '10.0.0.0/24', '10.0.1.1')
    add_route(r2, '10.0.3.0/24', '10.0.1.1')

    print('Running ping tests')
    result = ""

    result += "h1 to h3\n"
    result += h1.cmd('ping -c 1 10.0.2.2')

    result += "h2 to h3\n"
    result += h2.cmd('ping -c 1 10.0.2.2')

    result += "h3 to h1\n"
    result += h3.cmd('ping -c 1 10.0.0.1')

    result += "h3 to h2\n"
    result += h3.cmd('ping -c 1 10.0.3.4')

    with open('result1.txt', 'w') as f:
        f.write(result)

    print('Stopping network')
    net.stop()

if __name__ == '__main__':
    run()
