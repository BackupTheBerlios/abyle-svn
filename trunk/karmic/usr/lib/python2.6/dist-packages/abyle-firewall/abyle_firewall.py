import re
import os
import string
import time
import datetime
import sys
from abyle_output import abyle_output
from abyle_xmlparser import abyleparse
from abyle_execute import abyle_execute
from abyle_config_xmlparser import abyle_config_parse
from xml.sax.handler import ContentHandler
from xml.sax import make_parser


class abyle_firewall:
    def __init__(self, dryrun, iptablesbin, fwconfigpath, rulesfile, ipt_xmlconfig, xmlconfig, echocmd, logfile, verbose):
        self.naptime = 10 # milliseconds
        self.dryrun = dryrun
        self.iptablesbin = iptablesbin
        self.fwconfigpath = fwconfigpath
        self.rulesfile = rulesfile
        self.ipt_xmlconfig = ipt_xmlconfig
        self.xmlconfig = xmlconfig
        self.logfile = logfile
        self.verbose = verbose

        self.executioner = abyle_execute()

        self.echocmd = echocmd

        global_config = abyle_config_parse(fwconfigpath, "default", xmlconfig)

        self.excludedInterfaces = global_config.getConfig("excluded_interfaces")

        try:
            self.tcpabort_file = global_config.getConfig("tcpabortfile")
        except IndexError:
            self.tcpabort_file = "/proc/sys/net/ipv4/tcpicmpbcastfile_abort_on_overflow"

        try:
            self.icmpbcastreply_file = global_config.getConfig("icmpbcastfile")
        except IndexError:
            self.icmpbcastreply_file = "/proc/sys/net/ipv4/icmp_echo_ignore_broadcasts"

        try:
            self.dynaddresshack_file = global_config.getConfig("dynaddresshackfile")
        except IndexError:
            self.dynaddresshack_file = "/proc/sys/net/ipv4/ip_dynaddr"

        try:
            self.ipv4conf_path = global_config.getConfig("ipv4confpath")
        except IndexError:
            self.ipv4conf_path = "/proc/sys/net/ipv4/conf/"

        try:
            self.antispoofing_file = global_config.getConfig("antispoofingfile")
        except IndexError:
            self.antispoofing_file = "rp_filter"

        try:
            self.syncookiefile =  global_config.getConfig("syncookiefile")
        except IndexError:
            self.syncookiefile = "/proc/sys/net/ipv4/tcp_syncookies"

        try:
            self.ipv4forwardfile = global_config.getConfig("ipv4forwardfile")
        except IndexError:
            self.ipv4forwardfile = "/proc/sys/net/ipv4/ip_forward"

        try:
            self.syncookie = str(global_config.getConfig("syncookie")).upper()
        except IndexError:
            self.syncookie = "YES"

        try:
            self.ipv4forward = str(global_config.getConfig("ipv4forward")).upper()
        except IndexError:
            self.syncookie = "NO"

        try:
            self.tcpabort = str(global_config.getConfig("aborttcp")).upper()
        except IndexError:
            self.tcpabort = "NO"

        try:
            self.icmpbcastreply = str(global_config.getConfig("answericmpbroadcast")).upper()
        except IndexError:
            self.icmpbcastreply = "NO"

        try:
            self.dynaddresshack = str(global_config.getConfig("dynaddresshack")).upper()
        except IndexError:
            self.dynaddresshack = "NO"


        try:
            self.proxyarp_file = global_config.getConfig("proxyarpfile")
        except IndexError:
            self.proxyarp_file = "proxy_arp"

        try:
            self.srouting_file = global_config.getConfig("sroutingfile")
        except IndexError:
            self.srouting_file = "accept_source_route"

        try:
            self.icmpredirects_file = global_config.getConfig("icmprdrsfile")
        except IndexError:
            self.icmpredirects_file = "accept_redirects"

        try:
            self.secureicmpredirects_file = global_config.getConfig("icmpsecurerdrsfile")
        except IndexError:
            self.secureicmpredirects_file = "secure_redirects"

        try:
            self.martians_file = global_config.getConfig("martiansfile")
        except IndexError:
            self.martians_file = "log_martians"

        try:
            self.bootprelay_file = global_config.getConfig("bootprelayfile")
        except IndexError:
            self.bootprelay_file = "bootp_relay"



        now = datetime.datetime.now()
        now =  now.strftime("%Y/%m/%d %H:%M:%S")
        abyle_output("", "", "", "","blue", self.logfile, self.verbose)
        abyle_output("", "", "", "######################################### STARTUP #########################################","green", self.logfile, self.verbose)
        abyle_output("", "", "", "","blue", self.logfile, self.verbose)
        abyle_output("", "", "", "startup time: "+now,"default", self.logfile, self.verbose)
        abyle_output("", "", "", "","blue", self.logfile, self.verbose)

        abyle_output("","","","IPv4 send RST on full tcp buffer:", "blue", self.logfile, self.verbose)

        if not self.tcpabort == "NO":
            stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.tcpabort_file, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 send TCP-RST on full buffer is activated","default", self.logfile, self.verbose)
        else:
            stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.tcpabort_file, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 send TCP-RST on full buffer is deactivated","default", self.logfile, self.verbose)

        abyle_output("","","","IPv4 Reply to ICMP Broadcast:", "blue", self.logfile, self.verbose)

        if not self.icmpbcastreply == "NO":
            stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.icmpbcastreply_file, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 reply to ICMP Broadcasts is deactivated","default", self.logfile, self.verbose)
        else:
            stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.icmpbcastreply_file, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 reply to ICMP Broadcasts is activated","default", self.logfile, self.verbose)

        abyle_output("","","","IPv4 Dynamic-Address-Hack:", "blue", self.logfile, self.verbose)

        if not self.dynaddresshack == "NO":
            stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.dynaddresshack_file, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 dynamic address hack activated","default", self.logfile, self.verbose)
        else:
            stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.dynaddresshack_file, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 dynamic address hack deactivated","default", self.logfile, self.verbose)

        abyle_output("","","","IPv4 FORWARDING:", "blue", self.logfile, self.verbose)

        if not self.ipv4forward == "NO":
            stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4forwardfile, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 forwarding activated","default", self.logfile, self.verbose)
        else:
            stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4forwardfile, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "ipv4 forwarding deactivated","default", self.logfile, self.verbose)

        abyle_output("","","","SYNCOOKIE:", "blue", self.logfile, self.verbose)

        if not self.syncookie == "NO":
            stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.syncookiefile, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "syncookie activated","default", self.logfile, self.verbose)
        else:
            stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.syncookiefile, self.dryrun)
            abyle_output("abyle_firewall", stdErr, stdOut, "syncookie deactivated","default", self.logfile, self.verbose)

        self.default_config = abyleparse(self.fwconfigpath, "default", self.rulesfile, self.ipt_xmlconfig, self.excludedInterfaces)
        self.defaultrules =  self.default_config.getDefaultRules("head")

        for drule in self.defaultrules:
            abyle_output("abyle_firewall_buildUpFinish_head", "", "", "default-rule: "+drule,"default", self.logfile, self.verbose)
            stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+drule, self.dryrun)

    def check_well_formedness(self, file):
        try:
            saxparser = make_parser()
            saxparser.setContentHandler(ContentHandler())
            saxparser.parse(file)
            return "ok"
        except (Exception):
            return str(file) + " is NOT well-formed! " + sys.exc_info()[1]


    def buildUpFinish(self, verbose):
        self.verbose = verbose

        now = datetime.datetime.now()
        now =  now.strftime("%Y/%m/%d %H:%M:%S")
        self.defaultrules =  self.default_config.getDefaultRules("foot")
        abyle_output("","","","SETTING UP DEFAULT RULES:", "blue", self.logfile, self.verbose)
        for drule in self.defaultrules:
            abyle_output("abyle_firewall_buildUpFinish_foot", "", "", "default-rule: "+drule, "default", self.logfile, self.verbose)
            stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+drule, self.dryrun)
        abyle_output("", "", "", "", "blue", self.logfile, self.verbose)
        abyle_output("", "", "", "Startup done - "+now,"blue", self.logfile, self.verbose)
        abyle_output("", "", "", "", "blue", self.logfile, self.verbose)
        abyle_output("", "", "", "######################################### END #########################################","green", self.logfile, self.verbose)
        abyle_output("", "", "", "", "blue", self.logfile, self.verbose)


    def buildUp(self,protectedif,fwconfigpath, verbose):
        self.verbose = verbose


        self.protectedif = protectedif
        self.fwconfigpath = fwconfigpath
        abyle_output("", "", "", "", "blue", self.logfile, self.verbose)
        abyle_output("", "", "", "", "blue", self.logfile, self.verbose)
        abyle_output("", "", "", "Interface: "+self.protectedif, "green", self.logfile, self.verbose)
        abyle_output("", "", "", "", "blue", self.logfile, self.verbose)
        abyle_output("", "", "", "", "blue", self.logfile, self.verbose)

        if not self.verbose:
            self.output = abyle_output("","","","","default", self.logfile, self.verbose)
            self.output.startup("securing "+self.protectedif)

        if os.path.exists(self.fwconfigpath+'/'+'interfaces/'+self.protectedif) or self.excludedInterfaces.count(self.protectedif) > 0:

            if self.excludedInterfaces.count(self.protectedif) == 0:

                tempFileStr = self.fwconfigpath+'interfaces/'+self.protectedif+'/'+self.xmlconfig
                checkWellformed = self.check_well_formedness(tempFileStr)
                if checkWellformed != "ok":
                    abyle_output("","","",checkWellformed, "red", self.logfile, self.verbose)
                    sys.exit(1)
                else:
                    abyle_output("","","",self.fwconfigpath+'interfaces/'+self.protectedif+'/'+self.xmlconfig + " is a well-formed xml", "green", self.logfile, self.verbose)


                #parse the config file
                self.if_config = abyle_config_parse(self.fwconfigpath, self.protectedif, self.xmlconfig)

                try:
                    self.antispoofing = self.if_config.getConfig("antispoofing")
                except IndexError:
                    self.antispoofing = "NO"

                try:
                    self.proxyarp = self.if_config.getConfig("proxyarp")
                except IndexError:
                    self.proxyarp = "NO"

                try:
                    self.srouting = self.if_config.getConfig("sourcerouting")
                except IndexError:
                    self.srouting = "NO"

                try:
                    self.icmprdrs = self.if_config.getConfig("icmpredirects")
                except IndexError:
                    self.icmprdrs = "NO"

                try:
                    self.sicmprdrs = self.if_config.getConfig("secureicmpredirects")
                except IndexError:
                    self.sicmprdrs  = "NO"

                try:
                    self.martians = self.if_config.getConfig("martianslogging")
                except IndexError:
                    self.martians = "NO"

                try:
                    self.bootprelay = self.if_config.getConfig("drop0slash8packets")
                except IndexError:
                    self.bootprelay = "NO"

                try:
                    self.logging = self.if_config.getConfig("logging")
                except IndexError:
                    self.logging = "NO"

                try:
                    self.allowping = self.if_config.getConfig("allowping")
                except IndexError:
                    self.allowping = "NO"

                try:
                    self.masquerading = self.if_config.getConfig("masquerading")
                except IndexError:
                    self.masquerading = "NO"

                try:
                    self.portforwarding = self.if_config.getConfig("portforwarding")
                except IndexError:
                    self.portforwarding = "NO"

                try:
                    self.tproxy = self.if_config.getConfig("transparent_proxy")
                except IndexError:
                    self.tproxy = "NO"

                # end parse the config file



                self.antispoofing = str(self.antispoofing).upper()
                self.proxyarp = str(self.proxyarp).upper()
                self.srouting = str(self.srouting).upper()
                self.icmprdrs = str(self.icmprdrs).upper()
                self.sicmprdrs = str(self.sicmprdrs).upper()
                self.martians = str(self.martians).upper()
                self.bootprelay = str(self.bootprelay).upper()
                self.logging = str(self.logging).upper()
                self.allowping = str(self.allowping).upper()
                self.masquerading = str(self.masquerading).upper()
                self.portforwarding = str(self.portforwarding).upper()
                self.tproxy = str(self.tproxy).upper()


                # interface specific protections

                abyle_output("","","","PROXY ARP:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.proxyarp == "YES":
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4conf_path+self.protectedif+'/'+self.proxyarp_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "proxy arp activated for "+self.protectedif+"","default", self.logfile, self.verbose)
                else:
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4conf_path+self.protectedif+'/'+self.proxyarp_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "proxy arp deactivated for "+self.protectedif+"","default", self.logfile, self.verbose)

                abyle_output("","","","SOURCE ROUTING:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.srouting == "YES":
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4conf_path+self.protectedif+'/'+self.srouting_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "allow source routing activated for "+self.protectedif+"","default", self.logfile, self.verbose)
                else:
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4conf_path+self.protectedif+'/'+self.srouting_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "allow source routing deactivated for "+self.protectedif+"","default", self.logfile, self.verbose)

                abyle_output("","","","ICMP REDIRECTS:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.icmprdrs == "YES":
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4conf_path+self.protectedif+'/'+self.icmpredirects_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "icmp redirects activated for "+self.protectedif+"","default", self.logfile, self.verbose)
                else:
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4conf_path+self.protectedif+'/'+self.icmpredirects_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "icmp redirects deactivated for "+self.protectedif+"","default", self.logfile, self.verbose)

                abyle_output("","","","SECURE ICMP REDIRECTS:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.sicmprdrs == "YES":
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4conf_path+self.protectedif+'/'+self.secureicmpredirects_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "secure icmp redirects activated for "+self.protectedif+"","default", self.logfile, self.verbose)
                else:
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4conf_path+self.protectedif+'/'+self.secureicmpredirects_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "secure icmp redirects deactivated for "+self.protectedif+"","default", self.logfile, self.verbose)

                abyle_output("","","","LOG MARTIAN-IPs:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.martians == "YES":
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4conf_path+self.protectedif+'/'+self.martians_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "martians logging activated for "+self.protectedif+"","default", self.logfile, self.verbose)
                else:
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4conf_path+self.protectedif+'/'+self.martians_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "martians logging deactivated for "+self.protectedif+"","default", self.logfile, self.verbose)

                abyle_output("","","","Drop 0/8 packets.", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.bootprelay == "YES":
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4conf_path+self.protectedif+'/'+self.bootprelay_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "dropping packets from 0/8 activated for "+self.protectedif+"","default", self.logfile, self.verbose)
                else:
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4conf_path+self.protectedif+'/'+self.bootprelay_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "dropping packets from 0/8 deactivated for "+self.protectedif+"","default", self.logfile, self.verbose)






                abyle_output("","","","ANTI SPOOFING:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.antispoofing == "YES":
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 1 > '+self.ipv4conf_path+self.protectedif+'/'+self.antispoofing_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "anti spoofing for "+self.protectedif+" activated","default", self.logfile, self.verbose)
                else:
                    stdOut, stdErr = self.executioner.run(self.echocmd+' 0 > '+self.ipv4conf_path+self.protectedif+'/'+self.antispoofing_file, self.dryrun)
                    abyle_output("abyle_firewall_buildUp", stdErr, stdOut, "anti spoofing for "+self.protectedif+" deactivated","default", self.logfile, self.verbose)


            self.if_config = abyleparse(self.fwconfigpath, self.protectedif, self.rulesfile, self.ipt_xmlconfig, self.excludedInterfaces)
            self.rules =  self.if_config.getRules()
            abyle_output("","","","RULES:", "blue", self.logfile, self.verbose)
            if not self.verbose:
                self.output.startup(".")

            for rule in self.rules:
                time.sleep(self.naptime / 1000.0)
                abyle_output("abyle_firewall_buildUp_rules", "", "", self.protectedif+" "+rule,"default", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+rule, self.dryrun)

            if self.excludedInterfaces.count(self.protectedif) > 0:
                abyle_output("","","","", "blue", self.logfile, self.verbose)
                abyle_output("","","","interface "+self.protectedif+" excluded.", "green", self.logfile, self.verbose)
                abyle_output("","","","", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    try:
                        con_size = string.join(os.popen("stty size 2>/dev/null").readlines())
                        arr_con_size = string.split(con_size," ")
                        size = string.atoi(arr_con_size[1])-13
                        size = size+4
                        a = string.join(os.popen("echo -n \033[$(("+str(size)+"))G && echo -n    [EXCLUDED]  "))
                        self.output.startup(a, "green", "yes")
                    except IndexError:
                        self.output.startup("[EXCLUDED]\n")

            if self.excludedInterfaces.count(self.protectedif) == 0:

                abyle_output("","","","PORTFORWARDING:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.portforwarding == "YES":
                    self.portforwarding = self.if_config.getPortforwarding()
                    for portfwd in self.portforwarding:
                        abyle_output("abyle_firewall_buildUp_portfwd", "", "", self.protectedif+" "+portfwd, "default", self.logfile, self.verbose)
                        stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+portfwd, self.dryrun)
                else:
                    abyle_output("abyle_firewall_buildUp_portfwd", "", "", self.protectedif+" "+"PORTFORWARDING DISABLED", "default", self.logfile, self.verbose)

                abyle_output("","","","TRANSPARENT PROXY:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")

                if self.tproxy == "YES":
                    self.tproxy = self.if_config.getTproxy()
                    for transproxy in self.tproxy:
                        abyle_output("abyle_firewall_buildUp_transproxy", "", "", self.protectedif+" "+transproxy, "default", self.logfile, self.verbose)
                        stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+transproxy, self.dryrun)
                else:
                    abyle_output("abyle_firewall_buildUp_tproxy", "", "", self.protectedif+" "+"TRANSPARENT PROXY DISABLED", "default", self.logfile, self.verbose)


                    abyle_output("","","","LOGGING:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")
                if self.logging == "YES":
                    self.logging = self.if_config.getLogging()
                    for log in self.logging:
                        abyle_output("abyle_firewall_buildUp_log", "", "", self.protectedif+" "+log, "default", self.logfile, self.verbose)
                        stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+log, self.dryrun)
                else:
                    abyle_output("abyle_firewall_buildUp_logging", "", "", self.protectedif+" "+"LOGGING DISABLED", "default", self.logfile, self.verbose)

                abyle_output("","","","ALLOW PING:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")
                if self.allowping == "YES":
                    self.allowping = self.if_config.getAllowPing()
                    for ap in self.allowping:
                        abyle_output("abyle_firewall_buildUp_allowping", "", "", self.protectedif+" "+ap, "default", self.logfile, self.verbose)
                        stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+ap, self.dryrun)
                else:
                    abyle_output("abyle_firewall_buildUp_allowping", "", "", self.protectedif+" "+"ALLOWPING DISABLED", "default", self.logfile, self.verbose)

                abyle_output("","","","MASQUERADING:", "blue", self.logfile, self.verbose)
                if not self.verbose:
                    self.output.startup(".")
                if self.masquerading == "YES":
                    self.masquerading = self.if_config.getMasquerading()
                    for mg in self.masquerading:
                        abyle_output("abyle_firewall_buildUp_masquerading", "", "", self.protectedif+" "+mg, "default", self.logfile, self.verbose)
                        stdOut, stdErr = self.executioner.run(self.iptablesbin+' '+mg, self.dryrun)
                else:
                    abyle_output("abyle_firewall_buildUp_masquerading", "", "", self.protectedif+" "+"MASQUERADING DISABLED", "default", self.logfile, self.verbose)
                if not self.verbose:
                    try:
                        con_size = string.join(os.popen("stty size 2>/dev/null").readlines())
                        arr_con_size = string.split(con_size," ")
                        size = string.atoi(arr_con_size[1])-13
                        size = size+4
                        a = string.join(os.popen("echo -n \033[$(("+str(size)+"))G && echo -n    [DONE]  "))
                        self.output.startup(a, "blue", "yes")

                    except IndexError:
                        self.output.startup("[DONE]\n")



                                #self.output.startup("[DONE]", "blue")
        else:
            abyle_output("abyle_firewall", "", "", "ERROR: No directory found for interface "+self.protectedif+" in "+self.fwconfigpath+'interfaces/', "red", self.logfile, self.verbose)
