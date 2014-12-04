""" Teste ExaBGP

authors: Rafael S. Guimaraes (rafaelg@ifes.edu.br)

Four switches connected:


             R2 
             |  \
             |   \           
          |    \
      h1 --- R1 --- R3
        \          / 
          \-  R4  -/      		   
"""

from mininet.topo import Topo

class ExaBGPTest(Topo):
    """
    ExaBGP Test
    """
    def __init__(self):
	"""
	Create custom topo.
	"""

	Topo.__init__(self)
	
	h1 = self.addHost(
	    "h1",
	    ip="172.31.1.100/24",
	    defaultRoute="gw 172.31.1.1")
	r01 = self.addHost(
	    "r01",
	    ip="172.31.1.1/24")
	r02 = self.addHost(
	    "r02",
	    ip="10.0.2.1/24")
	r03 = self.addHost(
	    "r03",
	    ip="10.0.3.1/24")
	r04 = self.addHost(
	    "r04",
	    ip="10.0.4.1/24")
	# Switch 01 - Local Network A
	s1 = self.addSwitch("s1")
	# Switch 02 - Network r01 and r02
	s2 = self.addSwitch("s2")
	# Switch 03 - Network r01 and r03
	s3 = self.addSwitch("s3")
	# Switch 04 - Network r04 and r03
	s4 = self.addSwitch("s4")
	# Switch 05 - Network r02 and r03
	s5 = self.addSwitch("s5")
	
	# Add Hosts on switch on private LAN
	self.addLink(h1, s1)
	
	# Add Router on switch on LANs
	self.addLink(r01, s1)
	self.addLink(r01, s2)
	self.addLink(r01, s3)
	self.addLink(r04, s1)
	self.addLink(r04, s4)
	self.addLink(r02, s2)
	self.addLink(r02, s5)
	self.addLink(r03, s1)
	self.addLink(r03, s5)

topos = {'ExaBGPTest': (lambda: ExaBGPTest())}
