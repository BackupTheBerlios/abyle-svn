from xml import xpath
from xml.dom.minidom import *
import re
import sys
#from xml.dom.minidom import Node
from abyle_output import abyle_output

class abyleparse:
        def __init__(self, fwconfigpath, interface, rulesfile, ipt_xmlconfig):
                self.fwconfigpath = fwconfigpath
		self.pinterface = interface
		self.rulesfile = rulesfile
		self.iptflagsfile = ipt_xmlconfig
		self.rulesarray = []
		self.iptflags_dict = {}
 
		try:
			self.iptflags_config = xml.dom.minidom.parse(self.fwconfigpath+self.iptflagsfile).documentElement
			if self.pinterface == "default":
				self.rules_config = xml.dom.minidom.parse(self.fwconfigpath+self.rulesfile)
			else:
                		self.rules_config = xml.dom.minidom.parse(self.fwconfigpath+self.pinterface+'/'+self.rulesfile)
		except IOError, msg:
			abyle_output(self.interface+"_xmlparsing", "", "", str(msg))

	def compnum(self, x, y):
		DIGITS = re.compile(r'[0-9]+')
    		nx = ny = 0
    		while True:
       	 		a = DIGITS.search(x, nx)
        		b = DIGITS.search(y, ny)
        		if None in (a,b):
            			return cmp(x[nx:], y[ny:])
        		r = (cmp(x[nx:a.start()], y[ny:b.start()]) or
             			cmp(int(x[a.start():a.end()]), int(y[b.start():b.end()])))
        		if r:
            			return r
        		nx, ny = a.end(), b.end()

	def getIpTablesFlags(self):
		iptflags_dict_temp = {}

		interface_flag = xpath.Evaluate('/flags/flag[text()="interface"]/@cli_arg' , self.iptflags_config)
		interface_flag = interface_flag[0].value

		portforwarding_destination_flag = xpath.Evaluate('/flags/flag[text()="destination_portforwarding"]/@cli_arg' , self.iptflags_config)
		portforwarding_destination_flag = portforwarding_destination_flag[0].value

		transparent_toport_flag = xpath.Evaluate('/flags/flag[text()="toport_transproxy"]/@cli_arg' , self.iptflags_config)
		transparent_toport_flag = transparent_toport_flag[0].value

		outside_interface_flag = xpath.Evaluate('/flags/flag[text()="outside_interface"]/@cli_arg' , self.iptflags_config)
		outside_interface_flag = outside_interface_flag[0].value

		# get all flag nodes by xpath
		iptflag_nodes = xpath.Evaluate("/flags/flag", self.iptflags_config)

		# get all index attributes from flag tag nodes
		# fill dict with: index -> flag value (e.g. 1 -> interface)
		cnt = 0
                for node in iptflag_nodes:
                        attribute_nodes = xpath.Evaluate("./@index", iptflag_nodes[cnt])
                        self.attributestr = ""
                        for attribute in attribute_nodes:
				iptflags_dict_temp[attribute.value]=iptflag_nodes[cnt].firstChild.nodeValue
			cnt = cnt + 1

		# extract keys (index numbers) in an array and sort it
		indecies = iptflags_dict_temp.keys()
		indecies.sort(self.compnum)

		return iptflags_dict_temp, indecies, interface_flag, portforwarding_destination_flag, transparent_toport_flag, outside_interface_flag


	def flagCheck(self,flagvalue,flagname):
		self.flagvalue = flagvalue
		self.flagname = flagname

		if not self.flagvalue:
			self.flagstr = ''
		else:
			self.flagstr = self.flagname+' '+self.flagvalue+' '	
			
		return self.flagstr

	# an abstract method to parse xml traffic rules or portforwarding rules ... 
	def getAbstractXmlRules(self, xpathToMainNode):


		self.abstractRulesArray = []
		self.iptflags_indecies = []

		# parse the iptables flags config file, getIpTablesFlags returns:
		# -  a dict of iptablesflags e.g.: 11 -> destination or 12 -> destination-port
		# -  a sorted array of all available index numbers e.g: 1,2,3,...,12
		# -  the iptables cli switch for the interface argument: e.g: -i
		# -  special flag iptables cli switch for portforwarding destination
		# -  transparent proxy to-port flag
		# - masquerading interface flag (outside instead of inside)
		self.iptflags_dict, self.iptflags_indecies, interface, portfwdDestFlag, transproxyToPortFlag, outsideInterfaceFlag = self.getIpTablesFlags()

		if xpathToMainNode.find("masquerading") > 0:
			self.interfacestr = outsideInterfaceFlag+' '+self.pinterface+' '
		else:
			# set the interface string to e.g.: -i eth0
			self.interfacestr = interface+' '+self.pinterface+' '	

		# get list of rules e.g. all traffic nodes or all portforwarding nodes
		abstractNodes = xpath.Evaluate(xpathToMainNode, self.rules_config)


		cnt=0
		for node in abstractNodes:
			# get list of all attributes of an rule node
			abstractAttributeNodes = xpath.Evaluate("./@*", abstractNodes[cnt])
			self.attributestr = ""
			tempDestIpStr = ""
			tempDestPortStr = ""
			
			# loop through iptables flags index number list to build the right order 
			for indexNumber in self.iptflags_indecies:

				# get the value of a flag out if the iptables flag dict, e.g.: indexNumber=12 then flag_value = destination
				flag_value = self.iptflags_dict[indexNumber]
			
				# loop through all found attribute nodes	
				for attribute in abstractAttributeNodes:

					# thest if the attribute name is equal to the string in flag value
					if attribute.name == flag_value:

						try:
						  # parse the file with xpath and get the attributenode cli_arg which has the searched indexNumber
						  flag_cli_arg_node = xpath.Evaluate("/flags/flag[@index="+indexNumber+"]/@cli_arg", self.iptflags_config)

						  # extract the value if the attribute node [0] = assuming that the index is unique
						  flag_cli_arg = flag_cli_arg_node[0].firstChild.nodeValue

						  # check and build the attribute string with flagCheck()
						  attributeTmpstr = self.flagCheck(attribute.value,flag_cli_arg)	
						except KeyError, msg:
						  abyle_output("abyle_xmlparser.py: parsing error @ iptables flags:", "", "", str(msg), "red")
						  sys.exit(1)
					
						if xpathToMainNode.find("portforwarding") > 0 and attribute.name == "destination" :
								tempDestIpStr = attribute.value

						elif xpathToMainNode.find("portforwarding") > 0 and attribute.name == "destination-port":
								tempDestPortStr = attribute.value

						elif xpathToMainNode.find("transproxy") > 0 and attribute.name == "destination":
							tempDestIpStr = attribute.value

						elif xpathToMainNode.find("transproxy") > 0 and attribute.name == "destination-port":
							tempDestPortStr = attribute.value

						else:
							# append the temp string to the self.attributestr	
							self.attributestr = self.attributestr+attributeTmpstr

			cnt = cnt + 1


			if xpathToMainNode.find("portforwarding") > 0:

				# append interface string to the attribute string
				self.attributestr = self.interfacestr+self.attributestr+portfwdDestFlag+' '+tempDestIpStr+":"+tempDestPortStr

			elif xpathToMainNode.find("transproxy") > 0:
				self.attributestr = self.interfacestr+self.attributestr+transproxyToPortFlag+' '+tempDestPortStr

			else:
				self.attributestr = self.interfacestr+self.attributestr
	
			# append the string to the rules array
			self.abstractRulesArray.append(self.attributestr)	

		return self.abstractRulesArray
							
						
			


	def getRules(self):

		self.rulesarray = []
		self.rulesarray = self.getAbstractXmlRules("//interface/rules/traffic")
		return	self.rulesarray

	def getPortforwarding(self):

		self.rulesarray = []
		self.rulesarray = self.getAbstractXmlRules("//interface/portforwarding/traffic")
		
		return  self.rulesarray

	def getTproxy(self):

		self.rulesarray = []

		self.rulesarray = self.getAbstractXmlRules("//interface/transproxy/traffic")

		return self.rulesarray


	def getLogging(self):

		self.rulesarray = []

		self.rulesarray = self.getAbstractXmlRules("/interface/logging/traffic")

		return self.rulesarray

	def getDefaultRules(self, headOrFoot):

		self.rulesarray = []


		self.rulesarray = self.getAbstractXmlRules("/interface/blockrules"+headOrFoot+"/traffic")


		return self.rulesarray


	def getAllowPing(self):

		self.rulesarray = []

		self.rulesarray = self.getAbstractXmlRules("/interface/allowping/traffic")

		return self.rulesarray

	def getMasquerading(self):

		self.rulesarray = []

		self.rulesarray = self.getAbstractXmlRules("/interface/masquerading/traffic")

		return self.rulesarray