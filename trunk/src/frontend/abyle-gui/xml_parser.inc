<?php
function xml_loadfile($file) {
	$doc = domxml_open_file($file);
	$doc->formatOutput = true;
 	$doc->preserveWhiteSpace = false;
	return $doc;
}

function xml_getNode($doc, $NodeName) {
	$Node = $doc->get_elements_by_tagname($NodeName);
	return $Node;
}

function xml_getAttribute($Node, $AttributeName) {
	$AttributeValue = $Node->get_Attribute($AttributeName);
	return $AttributeValue;
}

function xml_setAttribute($Node, $AttributeName, $AttributeValue) {
	$Node->set_Attribute($AttributeName, $AttributeValue);
}
	
?>
