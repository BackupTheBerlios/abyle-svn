from xml import xpath
from xml.dom.minidom import *
doc = parse ("./iptables_flags.xml").documentElement
#traffic_nodes = xpath.Evaluate('/flags/flag[@index="2"]/@cli_arg', doc)
traffic_nodes = xpath.Evaluate('/flags/flag[text()="destination"]/@cli_arg', doc)

print traffic_nodes[0].value
