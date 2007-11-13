<?php include 'include/xml_parser.inc' ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>abyle::global config</title>
<link rel="stylesheet" href="2col_leftNav.css" type="text/css" />
</head>
<body>
<?php include 'include/global_nav.inc' ?>
<div id="content">
<?php 
$int_name = $_GET['interface'];
  echo '<div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=ic"> interface configuration </a> / <a href="ic_interface.php?interface='.$int_name.'">'.$int_name.' </a> /</div>';
?>
  <h2 id="pageName"><?php echo $int_name;?></h2>
    <h3>&nbsp;</h3>
	<?php
    echo '<table width="70%" id="table_gc_interfaces" style="table-layout:fixed">';
      echo '<tr>';
        echo '<td width="2%"><div align="left"><b>id</b></div></td>';
        echo '<td width="20%"><div align="left"><b>name</b></div></td>';
        echo '<td width="20%"><div align="left"><b>description</b></div></td>';
        echo '<td width="7%"><div align="left"><b>source</b></div></td>';
        echo '<td width="7%"><div align="left"><b>destination</b></div></td>';
        echo '<td width="7%"><div align="left"><b>dst-port</b></div></td>';
      echo '</tr>';
    echo '</table>';
    
  $id = 0;
	$sdoc = xml_loadfile($main_abyle_path.'/'.$int_name.'/'.$rules_file);
	foreach ($sdoc->rules->traffic as $rule) {
		$id++;
		$name = $rule['rulename'];
		$desc = $rule['desc'];
		$source = $rule['source'];
		$destination = $rule['destination'];
		$destination_port = $rule['destination-port'];
		
		if ($name == "") { $name = 'rule has no name'; }
    	echo '<table width="70%" id="table_gc_interfaces" style="table-layout:fixed">';
    	echo '<tr>';
        echo '<td width="2%"><div align="left">'.$id.'</div></td>';
        echo '<td width="20%"><div align="left"><a href="rule.php?interface='.$int_name.'&id='.$id.'">'.$name.'</a></div></td>';
        echo '<td width="20%"><div align="left">'.$desc.'</div></td>';
        echo '<td width="7%"><div align="left">'.$source.'</div></td>';
        echo '<td width="7%"><div align="left">'.$destination.'</div></td>';
        echo '<td width="7%"><div align="left">'.$destination_port.'</div></td>';
      	echo '</tr>';
    	echo '</table>';

    }
    ?>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
</div>
<div id="navBar">
<?php include 'include/nav.inc' ?>
<?php include 'include/nav_ic.inc' ?>
</div>
<?php include 'include/copyright.inc' ?>
<br />
</body>
</html>
