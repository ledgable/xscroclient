
<?php
	
	$ch = curl_init("<127.0.0.1>/api/<chainid>/buy/....");
	
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	
	$output = curl_exec($ch);
	curl_close($ch);
	
	echo $output;
	
?>
