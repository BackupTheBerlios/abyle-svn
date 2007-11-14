<?php
//header('Location: http://'. $_SERVER['SERVER_NAME'] .'/'); 
$extension=".php";
$link1 = $_GET["link"];
if (! empty($link1)) {
switch($link1) {
	case gc:
		header('Location: ./'.$link1.$extension);
		break;
	case status:
		header('Location: ./'.$link1.$extension);
		break;
	case ic:
		header('Location: ./'.$link1.$extension);
		break;
	case help:
		header('Location: ./'.$link1.$extension);
		break;
	case abyle:
		header('Location: ./'.$link1.$extension);
		break;
	case abyle-frontend:
		header('Location: ./'.$link1.$extension);
		break;
	case authors:
		header('Location: ./'.$link1.$extension);
		break;
	case rel_links:
		header('Location: ./'.$link1.$extension);
		break;
	case license:
		header('Location: ./'.$link1.$extension);
		break;
	case logfile:
		header('Location: ./'.$link1.$extension);
		break;
}
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>abyle::welcome</title>
<link rel="stylesheet" href="2col_leftNav.css" type="text/css" />
</head>
<body>
<?php include 'include/global_nav.inc' ?>
<div id="content">
  <div id="breadCrumb"> <a href="welcome.php">main </a> /</div>
  <h2 id="pageName">welcome to abyle </h2>
  <p>&nbsp;</p>
  <div class="feature"> <img src="images/abyle_logo.png" alt=""/>
    <h3>abyle - firewall based on iptables, written in python </h3>
    <h3>frontend  - written in php </h3>
    <h3></h3>
    <p> Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec molestie. Sed aliquam sem ut arcu. Phasellus sollicitudin. Vestibulum condimentum facilisis nulla. In hac habitasse platea dictumst. Nulla nonummy. Cras quis libero. Cras venenatis. Aliquam posuere lobortis pede. Nullam fringilla urna id leo. Praesent aliquet pretium erat. Praesent non odio. Pellentesque a magna a mauris vulputate lacinia. Aenean viverra. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Aliquam lacus. Mauris magna eros, semper a, tempor et, rutrum et, tortor. </p>
  	<p>&nbsp;</p>
	</div>
	<div align="center"><h6>abyle firewall supportet by</h6></div>
	<p><div align="center"><a href="http://developer.berlios.de" title="BerliOS Developer"> <img src="images/berliOS_small_logo.png" width="124px" height="32px" border="0" alt="BerliOS Developer Logo"></a></div></p>
	<p>&nbsp;</p>
</div>
<div id="navBar">
<?php include 'include/nav.inc' ?>
</div>
<?php include 'include/copyright.inc' ?>
<br />
</body>
</html>
