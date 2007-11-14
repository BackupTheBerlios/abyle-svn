<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>abyle::status</title>
<link rel="stylesheet" href="2col_leftNav.css" type="text/css" />
</head>
<body>
<?php include 'include/global_nav.inc' ?>
<div id="content">
  <div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=status"> status </a> / </div>
  <h2 id="pageName">status of abyle firewall</h2>
    <h3>&nbsp;</h3>
	<?php
	echo '<table width="300" id="table_rule" style="table-layout:fixed">';
	echo '<tr><td width="100">firewall is <b>active</b></td><td><img src="images/green.jpg" alt=""/></td></tr>';
	echo '</table>';
	echo '<br/>now must the daemon give me the output of "abyle --status"';
// 	exec('/usr/local/sbin/abyle --status',$output, $err);
// 	foreach ($output as $out_line) {
// 		echo $out_line.'<br>';
// 	}
	?>
	
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
</div>
<div id="navBar">
<?php include 'include/nav.inc' ?>
<?php include 'include/nav_status.inc' ?>
</div>
<?php include 'include/copyright.inc' ?>
<br />
</body>
</html>
