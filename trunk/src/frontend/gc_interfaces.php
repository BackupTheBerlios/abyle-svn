<?php include 'include/xml_parser.inc' ?>
<?php
$int = $_GET['interface'];
if (! empty($_GET['exclude'])) {
	$sdoc = xml_loadfile($main_abyle_path.'/'.$config_file);
	foreach ($sdoc->protect->interface as $interface) {
		if ($int == $interface) {
			$interface['excluded'] = $_GET['exclude'];
 		}
 	}
 	$sdoc->asXML($main_abyle_path.'/'.$config_file);
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>abyle::interfaces</title>
<link rel="stylesheet" href="2col_leftNav.css" type="text/css" />
</head>
<body>
<?php include 'include/global_nav.inc' ?>
<div id="content">
  <div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=gc"> global configuration </a> / <a href="gc_interfaces.php"> protected interfaces </a> /</div>
  <h2 id="pageName">protected interfaces   </h2>
  
    <h3>&nbsp;</h3>
	<?php
    echo '<table width="70%" id="table_gc_interfaces" style="table-layout:fixed">';
      echo '<tr>';
        echo '<td width="5%"><div align="left"><b>id</b></div></td>';
        echo '<td width="20%"><div align="left"><b>device</b></div></td>';
        echo '<td width="40%"><div align="left"><b>description</b></div></td>';
        echo '<td width="7%"><div align="left"><b>exclude</b></div></td>';
//        echo '<td width="23%"><div align="left"><b>task</b></div></td>';
      echo '</tr>';
    echo '</table>';
	
	$id = 0;
	$sdoc = xml_loadfile($main_abyle_path.'/'.$config_file);
	foreach ($sdoc->protect->interface as $interface) {
	$id++;
	$description = $interface['desc'];
	$excluded = $interface['excluded'];
	echo '<table width="70%" id="table_gc_interfaces" style="table-layout:fixed">';
      echo '<tr>';
        echo '<td width="5%"><div align="left">'.$id.'</div></td>';
        echo '<td width="20%"><div align="left">'.$interface.'</div></td>';
        echo '<td width="40%"><div align="left">'.$description.'</div></td>';
	    if ($excluded == 'yes') {
		  echo '<td width="7%"><form id="form1" name="form1" method="post" action="gc_interfaces.php?interface='.$interface.'&exclude=no">';
		} else {
		  echo '<td width="7%"><form id="form1" name="form1" method="post" action="gc_interfaces.php?interface='.$interface.'&exclude=yes">';
		}
		echo '<div align="left">';
			if ($excluded == 'yes') {
              echo '<input type="checkbox" name="excluded" value="checkbox" checked onclick="this.form.submit()"/>';
			} else {
			  echo '<input type="checkbox" name="excluded" value="checkbox" onclick="this.form.submit()"/>';
			}
            echo '</div>';
        echo '</form></td>';
//        echo '<td width="23%"><div align="left">remove</div></td>';
      echo '</tr>';
    echo '</table>';
	}
	?>

    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
  <div class="story"> </div>
</div>
<div id="navBar">
<?php include 'include/nav.inc' ?>
<?php include 'include/nav_gc.inc' ?>
</div>
<?php include 'include/copyright.inc' ?>
<br />
</body>
</html>
