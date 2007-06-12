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

		interface_flag = xpath.Evaluate('/flags[flag="interface"]/flag/@cli_arg' , self.iptflags_config)
		interface_flag = interface_flag[0].firstChild.nodeValue

		portforwarding_destination_flag = xpath.Evaluate('/flags/flag[flag="destination_portforwarding"]' , self.iptflags_config)
		print portforwarding_destination_flag	
		sys.exit(1)
		portforwarding_destination_flag = portforwarding_destination_flag[1].firstChild.nodeValue
		print "sdfsdfsd "+portforwarding_destination_flag

		# get all flag nodes by xpath
		iptflag_nodes = xpath.Evaluate("//flags/flag", self.iptflags_config)

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

		return iptflags_dict_temp, indecies, interface_flag, portforwarding_destination_flag


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
		self.iptflags_dict, self.iptflags_indecies, interface, portfwdDestFlag = self.getIpTablesFlags()

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
						  flag_cli_arg_node = xpath.Evaluate("//flags/flag[@index="+indexNumber+"]/@cli_arg", self.iptflags_config)

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

						else:
							# append the temp string to the self.attributestr	
							self.attributestr = self.attributestr+attributeTmpstr

			cnt = cnt + 1


			if xpathToMainNode.find("portforwarding") > 0:

				# append interface string to the attribute string
				self.attributestr = self.interfacestr+self.attributestr+portfwdDestFlag+tempDestIpStr+" "+tempDestPortStr

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

		self.iptflags_dict = self.getIpTablesFlags()

		self.interfacestr = self.iptflags_dict["interface_iptflag"]+' '+self.pinterface+' '

                for self.interface in self.rules_config.getElementsByTagName("interface"):

                        self.portforwarding_level = self.interface.getElementsByTagName("portforwarding")

                        for self.portforwarding in self.portforwarding_level:

                                self.traffic_level = self.portforwarding.getElementsByTagName("traffic")

                                for self.traffic in self.traffic_level:

					self.chainstr = self.flagCheck(self.traffic.getAttribute("chain"),self.iptflags_dict["chain_iptflag"])
					self.jobstr = self.flagCheck(self.traffic.getAttribute("job"),self.iptflags_dict["job_iptflag"])
					self.statestr = self.flagCheck(self.traffic.getAttribute("state"),self.iptflags_dict["state_iptflag"])
					self.sourcestr = self.flagCheck(self.traffic.getAttribute("source"),self.iptflags_dict["source_iptflag"])
					self.protocolstr = self.flagCheck(self.traffic.getAttribute("protocol"),self.iptflags_dict["protocol_iptflag"])

					self.destinationstr = self.flagCheck(self.traffic.getAttribute("destination"),self.iptflags_dict["todest_iptflag"])
					self.dportstr = self.flagCheck(self.traffic.getAttribute("destination-port"),"")

					self.tablestr = self.flagCheck(self.traffic.getAttribute("table"),self.iptflags_dict["table_iptflag"])
					self.forwardportstr = self.flagCheck(self.traffic.getAttribute("forward-port"),self.iptflags_dict["destination-port_iptflag"])


					self.destinationstr = re.sub("^[^\w]+","",self.destinationstr)
                                        self.destinationstr = re.sub("[^\w]+$","",self.destinationstr)
                                        self.destinationstr = '--'+self.destinationstr
	                                self.dportstr = re.sub("[^\w]+$","",self.dportstr)
	                                self.dportstr = re.sub("^[^\w]+","",self.dportstr)


					self.iptstr = self.tablestr+ \
						self.chainstr+ \
						self.protocolstr+ \
						self.forwardportstr+ \
						self.interfacestr+ \
						self.jobstr+ \
						self.destinationstr+':'+self.dportstr
					self.rulesarray.append(self.iptstr)

		return	self.rulesarray




	def getTproxy(self):

		self.rulesarray = []

		self.iptflags_dict = self.getIpTablesFlags()

		self.interfacestr = self.iptflags_dict["interface_iptflag"]+' '+self.pinterface+' '

                for self.interface in self.rules_config.getElementsByTagName("interface"):

                        self.tproxy_level = self.interface.getElementsByTagName("transproxy")

                        for self.tproxy in self.tproxy_level:

                                self.traffic_level = self.tproxy.getElementsByTagName("traffic")

                                for self.traffic in self.traffic_level:

					self.chainstr = self.flagCheck(self.traffic.getAttribute("chain"),self.iptflags_dict["chain_iptflag"])
					self.jobstr = self.flagCheck(self.traffic.getAttribute("job"),self.iptflags_dict["job_iptflag"])
					self.protocolstr = self.flagCheck(self.traffic.getAttribute("protocol"),self.iptflags_dict["protocol_iptflag"])
					self.dportstr = self.flagCheck(self.traffic.getAttribute("destination-port"),self.iptflags_dict["toport_iptflag"])
					self.tablestr = self.flagCheck(self.traffic.getAttribute("table"),self.iptflags_dict["table_iptflag"])
					self.forwardportstr = self.flagCheck(self.traffic.getAttribute("forward-port"),self.iptflags_dict["destination-port_iptflag"])

					self.iptstr = self.tablestr+ \
						self.chainstr+ \
						self.interfacestr+ \
						self.protocolstr+ \
						self.forwardportstr+ \
						self.jobstr+ \
						self.dportstr

					self.rulesarray.append(self.iptstr)

		return	self.rulesarray

	def getLogging(self):

		self.rulesarray = []

		self.iptflags_dict = self.getIpTablesFlags()

		self.interfacestr = self.iptflags_dict["interface_iptflag"]+' '+self.pinterface+' '

                for self.interface in self.rules_config.getElementsByTagName("interface"):

                        self.logging_level = self.interface.getElementsByTagName("logging")

                        for self.logging in self.logging_level:

                                self.log_level = self.logging.getElementsByTagName("traffic")

                                for self.traffic in self.log_level:

					
					self.chainstr = self.flagCheck(self.traffic.getAttribute("chain"),self.iptflags_dict["chain_iptflag"])
					self.jobstr = self.flagCheck(self.traffic.getAttribute("job"),self.iptflags_dict["job_iptflag"])
					self.protocolstr = self.flagCheck(self.traffic.getAttribute("protocol"),self.iptflags_dict["protocol_iptflag"])
					self.tcpflagsstr = self.flagCheck(self.traffic.getAttribute("tcp-flags"),self.iptflags_dict["tcpflags_iptflag"])
					self.destinationstr = self.flagCheck(self.traffic.getAttribute("destination"),self.iptflags_dict["destination_iptflag"])
					self.dportstr = self.flagCheck(self.traffic.getAttribute("destination-port"),self.iptflags_dict["destination-port_iptflag"])
					self.logprefixstr = self.flagCheck(self.traffic.getAttribute("prefix"),self.iptflags_dict["logprefix_iptflag"])
					self.limitstr = self.flagCheck(self.traffic.getAttribute("limit"),self.iptflags_dict["limit_iptflag"])

					if re.search('tcp', self.protocolstr):
						if self.tcpflagsstr:	
							self.protocolstr = self.protocolstr+' '+self.tcpflagsstr+' '

					if re.search('icmp', self.protocolstr):
						self.dportstr = ''

					self.iptstr = self.chainstr+ \
						self.interfacestr+ \
						self.protocolstr+ \
						self.destinationstr+ \
						self.dportstr+ \
						self.jobstr+ \
						self.logprefixstr+ \
						self.limitstr

					self.rulesarray.append(self.iptstr)

		return	self.rulesarray

	def getDefaultRules(self, headOrFoot):
		

		self.iptflags_dict = self.getIpTablesFlags()

		if headOrFoot == "head":
			self.rulesarray = []
			return self.rulesarray

			for self.interface in self.rules_config.getElementsByTagName("interface"):

                        	self.blockruleshead_level = self.interface.getElementsByTagName("blockruleshead")

                        	for self.blockruleshead in self.blockruleshead_level:
					self.blockchain = self.blockruleshead.getAttribute("blockchain")

                                	self.traffic_level = self.blockruleshead.getElementsByTagName("traffic")

                                	for self.traffic in self.traffic_level:
						self.chainstr = self.flagCheck(self.traffic.getAttribute("chain"),self.iptflags_dict["chain"])
						self.jobstr = self.flagCheck(self.traffic.getAttribute("job"),self.iptflags_dict["job"])
						self.statestr = self.flagCheck(self.traffic.getAttribute("state"),self.iptflags_dict["state"])
						self.newchainstr = self.flagCheck(self.blockchain,self.iptflags_dict["newchain"])

						self.rulesarray.append(self.newchainstr)

						self.iptstr = self.chainstr+ \
							self.statestr+ \
							self.jobstr

						self.rulesarray.append(self.iptstr)

			return	self.rulesarray


		if headOrFoot == "foot":
			self.rulesarray = []

			for self.interface in self.rules_config.getElementsByTagName("interface"):

                        	self.blockrulesfoot_level = self.interface.getElementsByTagName("blockrulesfoot")

                        	for self.blockrulesfoot in self.blockrulesfoot_level:

                                	self.traffic_level = self.blockrulesfoot.getElementsByTagName("traffic")

                                	for self.traffic in self.traffic_level:
						self.chainstr = self.flagCheck(self.traffic.getAttribute("chain"),self.iptflags_dict["chain"])
						self.jobstr = self.flagCheck(self.traffic.getAttribute("job"),self.iptflags_dict["job"])
						self.statestr = self.flagCheck(self.traffic.getAttribute("state"),self.iptflags_dict["state"])

						self.iptstr = self.chainstr+ \
							self.statestr+ \
							self.jobstr

						self.rulesarray.append(self.iptstr)
			return	self.rulesarray
					




	def getAllowPing(self):

		self.rulesarray = []

		self.iptflags_dict = self.getIpTablesFlags()

		self.interfacestr = self.iptflags_dict["interface_iptflag"]+' '+self.pinterface+' '

                for self.interface in self.rules_config.getElementsByTagName("interface"):

                        self.allowping_level = self.interface.getElementsByTagName("allowping")

                        for self.allowping in self.allowping_level:

                                self.traffic_level = self.allowping.getElementsByTagName("traffic")

                                for self.traffic in self.traffic_level:
					self.chainstr = self.flagCheck(self.traffic.getAttribute("chain"),self.iptflags_dict["chain"])
					self.jobstr = self.flagCheck(self.traffic.getAttribute("job"),self.iptflags_dict["job"])
					self.protocolstr = self.flagCheck(self.traffic.getAttribute("protocol"),self.iptflags_dict["protocol"])

					self.iptstr = self.chainstr+ \
						self.interfacestr+ \
						self.protocolstr+ \
						self.jobstr

					self.rulesarray.append(self.iptstr)

		return	self.rulesarray

	def getMasquerading(self):

		self.rulesarray = []

		self.iptflags_dict = self.getIpTablesFlags()

		self.interfacestr = self.iptflags_dict["outside_interface_iptflag"]+' '+self.pinterface+' '

                for self.interface in self.rules_config.getElementsByTagName("interface"):

                        self.masquerading_level = self.interface.getElementsByTagName("masquerading")

                        for self.masquerading in self.masquerading_level:

                                self.traffic_level = self.masquerading.getElementsByTagName("traffic")

                                for self.traffic in self.traffic_level:
					self.chainstr = self.flagCheck(self.traffic.getAttribute("chain"),self.iptflags_dict["chain_iptflag"])
					self.jobstr = self.flagCheck(self.traffic.getAttribute("job"),self.iptflags_dict["job_iptflag"])
					self.tablestr = self.flagCheck(self.traffic.getAttribute("table"),self.iptflags_dict["table_iptflag"])

					self.iptstr = self.chainstr+ \
						self.interfacestr+ \
						self.tablestr+ \
						self.jobstr

					self.rulesarray.append(self.iptstr)

		return	self.rulesarray
