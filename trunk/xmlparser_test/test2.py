from xml import xpath
from xml.dom.minidom import *
doc = parse ("/etc/abyle/iptables_flags.xml").documentElement
traffic_nodes = xpath.Evaluate("//flags/flag", doc)

cnt=0
for node in traffic_nodes:
	
	attribute_nodes = xpath.Evaluate("./@*", traffic_nodes[cnt])
	for attribute in attribute_nodes:
		print attribute.name+"   "+attribute.value,
	cnt = cnt + 1
	print
