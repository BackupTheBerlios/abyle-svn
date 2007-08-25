<?php
//header('Location: http://'. $_SERVER['SERVER_NAME'] .'/'); 
$extension=".php";
$link = $_GET["link"];
if (! empty($link)) {
switch($link) {
	case gc:
		header('Location: ./'.$link.$extension);
		break;
	case start_stop_restart:
		header('Location: ./'.$link.$extension);
		break;
	case ic:
		header('Location: ./'.$link.$extension);
		break;
	case help:
		header('Location: ./'.$link.$extension);
		break;
	case abyle:
		header('Location: ./'.$link.$extension);
		break;
	case abyle-frontend:
		header('Location: ./'.$link.$extension);
		break;
	case authors:
		header('Location: ./'.$link.$extension);
		break;
	case rel_links:
		header('Location: ./'.$link.$extension);
		break;
	case license:
		header('Location: ./'.$link.$extension);
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
<div id="masthead">
  <h1 id="siteName">abyle - frontend </h1>
  <div id="globalNav"> <a href="welcome.php">welcome</a>| <a href="welcome.php?link=abyle">what is abyle?</a>| <a href="welcome.php?link=abyle-frontend">what is abyle frontend?</a>| <a href="welcome.php?link=authors">authors</a>| <a href="welcome.php?link=rel_links">related links</a>| <a href="welcome.php?link=license">license</a>| <a href="http://www.abyle.org">abyle project home</a>|</div>
</div>
<h6>&nbsp;</h6>
<div id="content">
  <div id="breadCrumb"> <a href="welcome.php">main </a> /</div>
  <h2 id="pageName">welcome to abyle </h2>
  <div class="feature"> <img src="abyle_logo.jpg" alt="" width="150" height="150" />
    <h3>abyle - firewall based on iptables, written in python </h3>
    <p> Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec molestie. Sed aliquam sem ut arcu. Phasellus sollicitudin. Vestibulum condimentum facilisis nulla. In hac habitasse platea dictumst. Nulla nonummy. Cras quis libero. Cras venenatis. Aliquam posuere lobortis pede. Nullam fringilla urna id leo. Praesent aliquet pretium erat. Praesent non odio. Pellentesque a magna a mauris vulputate lacinia. Aenean viverra. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Aliquam lacus. Mauris magna eros, semper a, tempor et, rutrum et, tortor. </p>
  </div>
  <div class="story">
    <h3>Story Title</h3>
    <p> Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec molestie. Sed aliquam sem ut arcu. Phasellus sollicitudin. Vestibulum condimentum facilisis nulla. In hac habitasse platea dictumst. Nulla nonummy. Cras quis libero. Cras venenatis. Aliquam posuere lobortis pede. Nullam fringilla urna id leo. Praesent aliquet pretium erat. Praesent non odio. Pellentesque a magna a mauris vulputate lacinia. Aenean viverra. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Aliquam lacus. Mauris magna eros, semper a, tempor et, rutrum et, tortor. </p>
    <p> Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec molestie. Sed aliquam sem ut arcu. Phasellus sollicitudin. Vestibulum condimentum facilisis nulla. In hac habitasse platea dictumst. Nulla nonummy. Cras quis libero. Cras venenatis. Aliquam posuere lobortis pede. Nullam fringilla urna id leo. Praesent aliquet pretium erat. Praesent non odio. Pellentesque a magna a mauris vulputate lacinia. Aenean viverra. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Aliquam lacus. Mauris magna eros, semper a, tempor et, rutrum et, tortor. </p>
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
  
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
</div>
<div id="siteInfo"> <img src="abyle_logo_very_small.jpg" width="22" height="22" /><a href="#">frontend version 0.1</a> |<a href="mailto:nowx@abyle.org"> contact</a> | &copy; 2007 daniel schrammel</div>
<br />
</body>
</html>
