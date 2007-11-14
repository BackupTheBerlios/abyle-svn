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
$id = $_GET['id'];
$view_type = $_POST['view'];
if (isset($id)) {
	if ($id == 0) {
		$rule = $standard_view;
		drow_table($rule, $int_name, $id, $view_type, $standard_view, $extended_view);
	} else {
		$cnt = 0;
		$sdoc = xml_loadfile($main_abyle_path.'/'.$int_name.'/'.$rules_file);
		foreach ($sdoc->rules->traffic as $rule) {
				$cnt++;
				if ($id == $cnt) { drow_table($rule, $int_name, $id, $view_type, $standard_view, $extended_view); break; }
		}
	}
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

<?php
function drow_table($rule, $int_name, $id, $view_type, $standard_view, $extended_view) {
	if ($id == 0) {
		echo '<div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=ic"> interface configuration </a> / <a href="rule.php?id=0">add rule </a> /</div>';
		echo '<h2 id="pageName">add rule</h2>';
		if ($rule['rulename'] == "") { $rule['rulename'] = ''; }
	} else {	
		echo '<div id="breadCrumb"> <a href="welcome.php">main </a> / <a href="welcome.php?link=ic"> interface configuration </a> / <a href="ic_interface.php?interface='.$int_name.'">'.$int_name.' </a> /</div>';
		echo '<h2 id="pageName">'.$int_name.' - '.$rule['rulename'].'</h2>';
		if ($rule['rulename'] == "") { $rule['rulename'] = 'rule has no name'; }
	}
	echo '<h3>&nbsp;</h3>';
	echo '<form action="rule.php?interface='.$int_name.'&id='.$id.'" method="post">';
	echo '<table width="320" id="table_rule" style="table-layout:fixed">';
	echo '<tr><td width="155">';
	echo '<b>type of view:</b>';
	echo '</td><td bgcolor="#F3F3F3">';
	if ($view_type != "extended") {
		echo '<input type="radio" name="view" value="standard" checked="true"/>standard';
		echo '</td><td bgcolor="#F3F3F3">';
		echo '<input type="radio" name="view" value="extended" onclick="this.form.submit()"/>advanced';
	} else {
		echo '<input type="radio" name="view" value="standard" onclick="this.form.submit()"/>standard';
		echo '</td><td bgcolor="#F3F3F3">';
		echo '<input type="radio" name="view" value="extended" checked="true"/>advanced';
	}
	echo '</td></tr>';
	echo '</table>';
	echo '</form>';
	echo '<p>&nbsp;</p>';
	echo '<form action="rule.php" method="post" id="rule_form">';
		echo '<table width="400" id="table_rule" style="table-layout:fixed">';
		if ($view_type != "extended") { $view_type = $standard_view; } else { $view_type = array_merge($standard_view, $extended_view); }
		foreach ($view_type as $entry) {
		  echo '<tr>';
		    echo ('<td width="155"><div align="left"><b>'.$entry.': </b></div></td>');
				echo ('<td ><div align="left"><input class="text" type="text" name="'.$entry.'" id="'.$entry.'" maxlength="39" value="'.$rule[$entry].'" onblur="if(this.value==\'\') this.value=\''.$rule[$entry].'\'; this.style.backgroundColor=\'#F3F3F3\'" onfocus="this.style.backgroundColor=\'#ffffff\'; this.style.borderColor=\'#ffffff\'" /></div></td>');
		  echo '</tr>';
	  }
	  echo '</table>';
	echo '<br><input class="submit" type="submit" name="submit" value="- Save -">';
	echo '</form>';
}
