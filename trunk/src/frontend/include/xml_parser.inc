<?php
$standard_view = array('rulename','description', 'chain', 'job', 'state', 'source', 'destination', 'protocol', 'destination-port');
$extended_view = array('outside_interface', 'newchain', 'source-port_iptflag', 'forward-port', 'multiport_iptfalg', 'destination_portforwarding', 'toport_transproxy', 'logprefix', 'tcpfalgs', 'limit', 'icmp-type', 'recent', 'name', 'update', 'seconds', 'hitcount', 'set');
$main_abyle_path = '/etc/abyle';
$config_file = 'config.xml';
$rules_file = 'rules';
$ipt_flags_file = 'iptables_flags.xml';


function xml_loadfile($file) {
	if (file_exists($file)) {
		$s = simplexml_load_file($file);
		if (!$s) {
			echo 'ERROR parsing xml file: '.$file;
		} else {
			return $s;
		}
	} else { 
		echo $file.' does not exist! --> exit';
		exit;
	}
}

function xml_savefile($file, $sdoc) {
	if (file_exists($file)) {
		$sdoc->asXML($file);
	} else { 
		echo $file.' does not exist! --> exit';
		exit;
	}
}

?>
