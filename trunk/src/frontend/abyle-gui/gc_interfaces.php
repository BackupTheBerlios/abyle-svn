<?php include 'xml_parser.inc' ?>
<?php
$int = $_GET['interface'];
if (! empty($_GET['exclude'])) {
	$doc = xml_loadfile('/etc/abyle/config.xml');
	$Node = xml_getNode($doc, 'protect');
	foreach( $Node = xml_getNode($doc, 'interface') as $interface ) {
		if ($int == $interface->NodeValue) {
			xml_setAttribute($interface, 'excluded', $_GET['exclude']);
// 			$xmlfile = fopen('/etc/abyle/config.xml', 'w');
// 			fwrite($xmlfile, $doc);
		}
	}
}
?>
		
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>abyle::interface</title>
<link rel="stylesheet" href="2col_leftNav.css" type="text/css" />
</head>
<body>
<div id="masthead">
  <h1 id="siteName">abyle - frontend </h1>
  <div id="globalNav"> <a href="welcome.php">welcome</a>| <a href="welcome.php?link=abyle">what is abyle?</a>| <a href="welcome.php?link=abyle-frontend">what is abyle frontend?</a>| <a href="welcome.php?link=authors">authors</a>| <a href="welcome.php?link=rel_links">related links</a>| <a href="welcome.php?link=license">license</a>| <a href="http://www.abyle.org">abyle project home</a>|</div>
</div>
<h6>&nbsp;</h6>
<div id="content">
  <div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=gc"> global configuration </a> / <a href="gc_interfaces.php"> protected interfaces </a> /</div>
  <h2 id="pageName">protected interfaces   </h2>
  <div class="feature">
    <h3>&nbsp;</h3>
	<?php
    echo '<table width="50%" border="0" cellspacing="0" cellpadding="0">';
      echo '<tr>';
        echo '<th width="5%" scope="col"><div align="left">id</div></th>';
        echo '<th width="20%" scope="col"><div align="left">device</div></th>';
        echo '<th width="34%" scope="col"><div align="left">description</div></th>';
        echo '<th width="18%" scope="col"><div align="left">exclude</div></th>';
        echo '<th width="23%" scope="col"><div align="left">task</div></th>';
      echo '</tr>';
    echo '</table>';
    echo '<hr align="left" width="50%" />';
	
	$id = 0;
	$doc = xml_loadfile('/etc/abyle/config.xml');
	$Node = xml_getNode($doc, 'protect');
	foreach( $Node = xml_getNode($doc, 'interface') as $interface ) {
	$id++;
	$description = xml_getAttribute($interface, 'desc');
	$excluded = xml_getAttribute($interface, 'excluded');
	echo '<table width="50%" border="0" cellspacing="0" cellpadding="0">';
      echo '<tr>';
        echo '<td width="5%"><div align="left">'.$id.'</div></td>';
        echo '<td width="20%"><div align="left">'.$interface->NodeValue.'</div></td>';
        echo '<td width="34%"><div align="left">'.$description.'</div></td>';
	    if ($excluded == 'yes') {
		  echo '<td width="18%"><form id="form1" name="form1" method="post" action="gc_interfaces.php?interface='.$interface->NodeValue.'&exclude=no">';
		} else {
		  echo '<td width="18%"><form id="form1" name="form1" method="post" action="gc_interfaces.php?interface='.$interface->NodeValue.'&exclude=yes">';
		}
		echo '<div align="left">';
			if ($excluded == 'yes') {
              echo '<input type="checkbox" name="excluded" value="checkbox" checked onclick="this.form.submit()"/>';
			} else {
			  echo '<input type="checkbox" name="excluded" value="checkbox" onclick="this.form.submit()"/>';
			}
            echo '</div>';
        echo '</form>        </td>';
        echo '<td width="23%"><div align="left">remove</div></td>';
      echo '</tr>';
    echo '</table>';
    echo '<hr align="left" width="50%" />';
	}
	?>
    <table width="50%" border="0" cellpadding="0" cellspacing="0">
      <tr>
        <td width="5%"><div align="left"></div></td>
        <td width="20%"><div align="left"></div></td>
        <td width="34%"><div align="left">
          <form id="form2" name="form2" method="post" action="">
          </form>
          </div></td>
        <td width="18%"><form id="form1" name="form1" method="post" action="">
            <div align="left"></div>
        </form></td>
        <td width="23%"><div align="left">add</div></td>
      </tr>
    </table>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
  </div>
  <div class="story"> </div>
</div>
<div id="navBar">
  <div id="sectionLinks">
    <ul>
      <li><a href="welcome.php?link=start_stop_restart">start / stop / restart </a></li>
      <li><a href="welcome.php?link=gc">global configuration </a></li>
      <li><a href="welcome.php?link=ic">interface configuration</a></li>
      <li><a href="welcome.php?link=help">help / documentation </a></li>
      <li></li>
    </ul>
  </div>
  <div class="relatedLinks"></div>
  
  <p class="relatedLinks">&nbsp;</p>
  <p class="relatedLinks"><strong>options</strong></p>
  <p class="relatedLinks"><a href="gc_features.php">available features</a> </p>
  <p class="relatedLinks"><a href="gc_interfaces.php">protected interfaces</a> </p>
  <p class="relatedLinks"><a href="gc_paths.php">paths</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
</div>
<div id="siteInfo"> <img src="abyle_logo_very_small.jpg" width="22" height="22" /><a href="#">frontend version 0.1</a> |<a href="mailto:nowx@abyle.org"> contact</a> | &copy; 2007 daniel schrammel</div>
<br />
</body>
</html>
