from xml.dom.minidom import *
import re
import sys
#from xml.dom.minidom import Node
from abyle_output import abyle_output

try:
    from oldxml import xpath
except (ImportError):
    abyle_output("xml parser import error, please install python xpath modules", "", "", str(sys.exc_info()[1]), "red")
    sys.exit(1)

class abyleparse:
    def __init__(self, fwconfigpath, interface, rulesfile, ipt_xmlconfig, excludedInterfaces):
        self.fwconfigpath = fwconfigpath
        self.pinterface = interface
        self.rulesfile = rulesfile
        self.iptflagsfile = ipt_xmlconfig
        self.rulesarray = []
        self.iptflags_dict = {}
        self.excludedInterfaces = excludedInterfaces
        self.allowping = ""

        try:
            self.iptflags_config = xml.dom.minidom.parse(self.fwconfigpath+self.iptflagsfile).documentElement
            if self.excludedInterfaces.count(self.pinterface) > 0:
                self.rules_config = xml.dom.minidom.parse(self.fwconfigpath+self.rulesfile)

            elif self.pinterface == "default":
                self.rules_config = xml.dom.minidom.parse(self.fwconfigpath+self.rulesfile)
            else:
                self.rules_config = xml.dom.minidom.parse(self.fwconfigpath+'interfaces/'+self.pinterface+'/'+self.rulesfile)
        except (IOError):
            abyle_output(self.pinterface+"_xmlparsing", "", "", sys.exc_info()[1])

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

        subflag_dict_temp = {}
        subflag_cliswitch_dict_temp = {}

        interface_flag = xpath.Evaluate('/flags/flag/cfgname[text()="interface"]/@cli_switch' , self.iptflags_config)
        interface_flag = interface_flag[0].value

        portforwarding_destination_flag = xpath.Evaluate('/flags/flag/cfgname[text()="destination_portforwarding"]/@cli_switch' , self.iptflags_config)
        portforwarding_destination_flag = portforwarding_destination_flag[0].value

        transparent_toport_flag = xpath.Evaluate('/flags/flag/cfgname[text()="toport_transproxy"]/@cli_switch' , self.iptflags_config)
        transparent_toport_flag = transparent_toport_flag[0].value

        outside_interface_flag = xpath.Evaluate('/flags/flag/cfgname[text()="outside_interface"]/@cli_switch' , self.iptflags_config)
        outside_interface_flag = outside_interface_flag[0].value

        # get all flag nodes by xpath
        iptflag_nodes = xpath.Evaluate("/flags/flag", self.iptflags_config)

        # get all index attributes from flag tag nodes
        # fill dict with: index -> flag value (e.g. 1 -> interface)
        cnt = 0
        for node in iptflag_nodes:
            subflags = ""
            attribute_nodes = xpath.Evaluate("./@index", iptflag_nodes[cnt])
            self.attributestr = ""
            for attribute in attribute_nodes:
                tempAtrribute = iptflag_nodes[cnt].getElementsByTagName('cfgname')[0].firstChild.nodeValue
                iptflags_dict_temp[attribute.value]=tempAtrribute
                subflags = xpath.Evaluate('/flags/flag/cfgname[text()="'+tempAtrribute+'"]/../subflag[text()]', self.iptflags_config)

                if len(subflags) > 0:
                    tempSubflags = ""
                    tempSubflagsCliSwitch = ""
                    sfcnt = 0
                    for subflag in subflags:
                        if sfcnt == 0:
                            tempSubflags = subflags[sfcnt].firstChild.nodeValue
                            tempSubflagsCliSwitch = subflags[sfcnt].getAttribute("cli_switch").strip()
                        else:
                            tempSubflags = tempSubflags+";"+subflags[sfcnt].firstChild.nodeValue
                            tempSubflagsCliSwitch = tempSubflagsCliSwitch+";"+subflags[sfcnt].getAttribute("cli_switch").strip()
                        sfcnt = sfcnt+1
                    subflag_dict_temp[attribute.value]=tempSubflags
                    subflag_cliswitch_dict_temp[attribute.value]=tempSubflagsCliSwitch

            cnt = cnt + 1


        return iptflags_dict_temp, interface_flag, portforwarding_destination_flag, transparent_toport_flag, outside_interface_flag, subflag_dict_temp, subflag_cliswitch_dict_temp


    def flagCheck(self,flagvalue,flagname, indexNumber, iptflags_config):
        self.flagvalue = flagvalue
        self.flagname = flagname
        valueSupport = ""

        # check if this flag supports values

        # this xpath expression selects the value arguemnt of the given cli_switch argument under the given index number
        valueSupport = xpath.Evaluate('/flags/flag[@index="'+indexNumber+'"]//*[@cli_switch="'+flagname+'"]/@value', iptflags_config)
        valueSupport = valueSupport[0].firstChild.nodeValue

        if valueSupport == "no":
            self.flagstr = self.flagname+' '
        else:

            if not self.flagvalue:
                self.flagstr = ''
            else:
                self.flagstr = self.flagname+' '+self.flagvalue+' '

        return self.flagstr

    # an abstract method to parse xml traffic rules or portforwarding rules ...
    def getAbstractXmlRules(self, xpathToMainNode):


        self.abstractRulesArray = []
        self.iptflags_indecies = []

        if self.allowping == "yes":
            self.rules_config = xml.dom.minidom.parse(self.fwconfigpath+self.rulesfile)

        if xpathToMainNode.find("masquerading") > 0:
            self.rules_config = xml.dom.minidom.parse(self.fwconfigpath+'interfaces/'+self.pinterface+'/'+self.rulesfile)

        # parse the iptables flags config file, getIpTablesFlags returns:
        # -  a dict of iptablesflags e.g.: 11 -> destination or 12 -> destination-port
        # -  a sorted array of all available index numbers e.g: 1,2,3,...,12
        # -  the iptables cli switch for the interface argument: e.g: -i
        # -  special flag iptables cli switch for portforwarding destination
        # -  transparent proxy to-port flag
        # -  masquerading interface flag (outside instead of inside)
        # -  subflag dictionary
        self.iptflags_dict, interface, portfwdDestFlag, transproxyToPortFlag, outsideInterfaceFlag, subflags_dict, subflags_cliswitch_dict = self.getIpTablesFlags()

        # extract keys (index numbers) in an array and sort it
        self.iptflags_indecies = self.iptflags_dict.keys()
        self.iptflags_indecies.sort(self.compnum)

        if xpathToMainNode.find("head") > 0:
            blockchain = xpath.Evaluate("/interface/blockruleshead/@blockchain", self.rules_config)
            blockchain = blockchain[0].firstChild.nodeValue
            blockchain_create_string = " -N "+blockchain
            self.abstractRulesArray.append(blockchain_create_string)


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
            tempForwardPortStr = ""





            # loop through iptables flags index number list to build the right order
            for indexNumber in self.iptflags_indecies:

                # get the value of a flag out if the iptables flag dict, e.g.: indexNumber=12 then flag_value = destination
                flag_value = self.iptflags_dict[indexNumber]

                # loop through all found attribute nodes
                for attribute in abstractAttributeNodes:

                    # test if the attribute name is equal to the string in flag value
                    if attribute.name == flag_value:

                        try:
                            # parse the file with xpath and get the attributenode cli_switch under cfgname which has the searched indexNumber
                            flag_cli_arg_node = xpath.Evaluate("/flags/flag[@index="+indexNumber+"]/cfgname/@cli_switch", self.iptflags_config)

                            # extract the value if the attribute node [0] = assuming that the index is unique
                            flag_cli_arg = flag_cli_arg_node[0].firstChild.nodeValue


                            # check and build the attribute string with flagCheck()
                            attributeTmpstr = self.flagCheck(attribute.value,flag_cli_arg, indexNumber, self.iptflags_config)



                        except (KeyError):
                            abyle_output("abyle_xmlparser.py: parsing error @ iptables flags:", "", "", sys.exc_info()[1], "red")
                            sys.exit(1)

                        if xpathToMainNode.find("portforwarding") > 0 and attribute.name == "destination" :
                            tempDestIpStr = attribute.value

                        elif xpathToMainNode.find("portforwarding") > 0 and attribute.name == "destination-port":
                            tempDestPortStr = attribute.value

                        elif xpathToMainNode.find("portforwarding") > 0 and attribute.name == "forward-port":
                            tempForwardPortStr = attribute.value

                        elif xpathToMainNode.find("transparentproxy") > 0 and attribute.name == "destination":
                            tempDestIpStr = attribute.value

                        elif xpathToMainNode.find("transparentproxy") > 0 and attribute.name == "destination-port":
                            tempDestPortStr = attribute.value

                        else:
                            # append the temp string to the self.attributestr
                            self.attributestr = self.attributestr+attributeTmpstr

                        hasSubflags = "no"
                        for key in subflags_dict.keys():
                            if str(key) == str(indexNumber):
                                hasSubflags = "yes"

                        if hasSubflags == "yes":
                            subattributeTmpstr = ""
                            tempSubflagsArray = subflags_dict[indexNumber].split(';')
                            tempSubflagsCliswitchArray = subflags_cliswitch_dict[indexNumber].split(';')

                            subflagcnt = 0
                            for subflag_value in tempSubflagsArray:

                                for attribute in abstractAttributeNodes:

                                    if attribute.name == subflag_value:

                                        subattributeTmpstr = self.flagCheck(attribute.value,tempSubflagsCliswitchArray[subflagcnt], indexNumber, self.iptflags_config)
                                        self.attributestr = self.attributestr+subattributeTmpstr

                                subflagcnt = subflagcnt + 1


            cnt = cnt + 1

            self.attributestrForward = ""

            if xpathToMainNode.find("portforwarding") > 0:

                # append interface string to the attribute string

                # build the iptablescommand for the PREROUTING chain of the nat table and the FORWARD chain
                if not self.pinterface == "default":
                    self.attributestr = self.interfacestr+self.attributestr


                self.attributestrForward = self.attributestr
                self.attributestrForward = re.sub("PREROUTING","FORWARD",self.attributestrForward)
                self.attributestrForward = re.sub("DNAT","ACCEPT",self.attributestrForward)
                self.attributestrForward = re.sub("-t nat","",self.attributestrForward)
                self.attributestrForward = re.sub("--dport \d{1,5}","",self.attributestrForward)
                self.attributestrForward = self.attributestrForward+" --destination-port "+tempDestPortStr+" --destination "+tempDestIpStr

                self.attributestr = self.attributestr+"--dport "+tempForwardPortStr+" "+portfwdDestFlag+' '+tempDestIpStr+":"+tempDestPortStr



            elif xpathToMainNode.find("transparentproxy") > 0:
                self.attributestr = self.interfacestr+self.attributestr+transproxyToPortFlag+' '+tempDestPortStr

            else:
                if not self.pinterface == "default":
                    self.attributestr = self.interfacestr+self.attributestr

            # append the string to the rules array
            self.abstractRulesArray.append(self.attributestr)

            if not self.attributestrForward == "":
                self.abstractRulesArray.append(self.attributestrForward)




        return self.abstractRulesArray





    def getRules(self):

        self.rulesarray = []
        if self.excludedInterfaces.count(self.pinterface) > 0:
            self.rulesarray = self.getAbstractXmlRules("/interface/excluderule/traffic")
        else:
            self.rulesarray = self.getAbstractXmlRules("/interface/rules/traffic")
        return  self.rulesarray

    def getPortforwarding(self):

        self.rulesarray = []
        self.rulesarray = self.getAbstractXmlRules("/interface/portforwarding/traffic")

        return  self.rulesarray

    def getTproxy(self):

        self.rulesarray = []

        self.rulesarray = self.getAbstractXmlRules("/interface/transparentproxy/traffic")

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

        self.allowping = "yes"

        self.rulesarray = self.getAbstractXmlRules("/interface/pingrule/traffic")

        self.allowping = ""


        return self.rulesarray

    def getMasquerading(self):

        self.allowping = ""

        self.rulesarray = []

        self.rulesarray = self.getAbstractXmlRules("/interface/masquerading/traffic")

        return self.rulesarray
