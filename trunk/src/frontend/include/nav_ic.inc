  <div class="relatedLinks"></div>
  
  <p class="relatedLinks">&nbsp;</p>
  <p class="relatedLinks"><strong>protected interfaces</strong></p>
  	<?php
	$sdoc = xml_loadfile($main_abyle_path.'/'.$config_file);
	$i = 0;
	foreach ($sdoc->protect->interface as $interface) {
		if ($interface['excluded'] == "no") {
			echo '<p class="relatedLinks"><a href="ic_interface.php?interface='.$interface.'">'.$interface.' ('.$interface['desc'].') </a></p>';
			$i = 1;
		}
	}
	if ($i == 0) {
		echo '<p class="relatedLinks">none</p>';
	}
	?>
  <p class="relatedLinks"><strong>unprotected interfaces</strong></p>
  <?php
  $i = 0;
	foreach ($sdoc->protect->interface as $interface) {
		if ($interface['excluded'] == "yes") {
			echo '<p class="relatedLinks"><a href="ic_interface.php?interface='.$interface.'">'.$interface.' ('.$interface['desc'].') </a></p>';
			$i = 1;
		}
	}
	if ($i == 0) {
		echo '<p class="relatedLinks">none</p>';
	}
	?>
  <p class="relatedLinks">&nbsp;</p>
  <p class="relatedLinks"><strong>options</strong></p>
  <p class="relatedLinks"><a href="rule.php?id=0">add rule</a></p>
  <p class="relatedLinks">&nbsp;</p>
  <p>&nbsp;</p>
