<?php include 'include/xml_parser.inc' ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>abyle::paths</title>
<link rel="stylesheet" href="2col_leftNav.css" type="text/css" />
</head>
<body>
<?php include 'include/global_nav.inc' ?>
<div id="content">
  <div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=gc"> global configuration </a> / <a href="gc_paths"> paths </a> /</div>
  <h2 id="pageName">paths  </h2>
   
    <?php
	echo '<form action="gc_paths.php" method="post" id="path_form">';
	echo '<table width="600" id="table_rule" style="table-layout:fixed">';
	echo '<input type="hidden" name="options_changed" value="true">';
    $sdoc = xml_loadfile($main_abyle_path.'/'.$config_file);
    foreach ($sdoc as $option) {
		if (! empty($option)) {
			echo '<tr>';
			echo '<td width="145"><b>'.$option->getName().'</b></td>';
		    echo ('<td><input width="600" class="text" name="'.$option->getName().'" type="text" size="35" value="'.$option.'" onblur="if(this.value==\'\') this.value=\''.$option.'\'; this.style.backgroundColor=\'#F3F3F3\'" onfocus="this.style.backgroundColor=\'#ffffff\'; this.style.borderColor=\'#ffffff\'"></td>');
			echo '</tr>';
		}
    }
    echo '</table>';
    echo '<br><input class="submit" type="submit" name="submit" value="- Save -">';
    echo '</form>';
    ?>


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
