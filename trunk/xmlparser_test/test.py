from xml import xpath
from xml.dom.minidom import *
doc = parse ("./iptables_flags.xml").documentElement
#traffic_nodes = xpath.Evaluate('/flags/flag[@index="2"]/@cli_arg', doc)
traffic_nodes = xpath.Evaluate('/flags/flag[flag="destination"]/@cli_arg', doc)

print traffic_nodes
cnt=0
for node in traffic_nodes:
	
	print node.value
