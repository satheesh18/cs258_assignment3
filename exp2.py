from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink

def run():
    net = Mininet(link=TCLink, switch=OVSKernelSwitch)

    print('Creating hosts')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')

    print('Creating switches')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    print('Creating links')
    # Link from s1-eth1 to s2-eth1
    net.addLink(s1, s2)

    # Link from h2-eth0 to s1-eth2
    net.addLink(h2, s1)

    # Link from h1-eth0 to s1-eth3
    net.addLink(h1, s1)

    # Link from s2-eth2 to h3-eth0
    net.addLink(s2, h3)

    print('Starting network')
    net.start()

    print('Network is ready. You can now inspect and configure switches')
    input('Press Enter after you are done testing switches')

    print('Running ping tests')
    result = ""

    result += "h1 to h3\n"
    result += h1.cmd('ping -c 1 10.0.0.3')

    result += "h2 to h3\n"
    result += h2.cmd('ping -c 1 10.0.0.3')

    with open('result2.txt', 'w') as f:
        f.write(result)

    print('Stopping network')
    net.stop()

if __name__ == '__main__':
    run()
