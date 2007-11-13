<?php
if ($_GET['clear'] == 1) {
	echo 'now must the daemon clear the logfile...';
}
?>
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
  <div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=logfile">logfile </a> / </div>
  <h2 id="pageName">logfile  </h2>

<?php
echo '<table width="70%" id="table_gc_interfaces" style="table-layout:fixed">';
$logfile = ('/var/log/abyle.log');
$handle = @fopen($logfile, 'r');
if ($handle) {
    while (!feof($handle)) {
        $buffer = fgets($handle, 4096);
        echo '<tr>';
        echo '<td><div align="left">'.$buffer.'</div></td>';
        echo '</tr>';
    }
    fclose($handle);
}
echo '</table>';
?>

</div>
<div id="navBar">
<?php include 'include/nav.inc' ?>
<?php include 'include/nav_logfile.inc' ?>
</div>
<?php include 'include/copyright.inc' ?>
<br />
</body>
</html>
