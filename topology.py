from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call

def topology():

    "Create a network."
    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/24')

    info("*** Creating nodes")
    #h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
    #h2 = net.addHost( 'h2', mac='00:00:00:00:00:11', ip='10.0.1.1/8' )

    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', position='50,50,0' )
    sta2 = net.addStation( 'sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', position='40,50,0')
    sta3 = net.addStation( 'sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8', position='20,50,0' )

    ap1 = net.addAccessPoint( 'ap1', ssid= 'new-ssid', mode= 'g', channel= '5', position='25,50,0', range='35' )
    ap2 = net.addAccessPoint( 'ap2', ssid= 'new-ssid', mode= 'g', channel= '10', position='45,50,0', range='35' )

    c1 = net.addController( 'c1' )

    #s3 = net.addSwitch('s3')

    #net.runAlternativeModule('../module/mac80211_hwsim.ko')

    info("*** Configuring wifi nodes")
    net.configureWifiNodes()

    info("*** Associating and Creating links")

    net.addLink(ap1, ap2)
    #net.addLink(ap1, s3)
    #net.addLink(ap2, s3)
    #net.addLink(s3, c1)
    #net.addLink(ap1, ap2)

    #net.addLink(s3, h1)
    #net.addLink(s3, h2)

    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)
    net.addLink(ap1, sta3)

    info( "*** Starting network")
    net.build()
    c1.start()
    ap1.start( [c1] )
    ap2.start( [c1] )
    #s3.start([c1])

    """uncomment to plot graph"""
    net.plotGraph(max_x=1000, max_y=1000)

    net.startMobility(startTime=0)
    net.mobility(sta1, 'start', time=1, position='0.0,50.0,0.0')
    net.mobility(sta1, 'stop', time=30, position='100.0,50.0,0.0')
    net.stopMobility(stopTime=31)

    info("*** Running CLI")
    CLI( net )

    info( "*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
