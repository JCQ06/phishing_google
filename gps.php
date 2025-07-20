<?php
$data = json_decode(file_get_contents("php://input"));
$lat = $data->lat;
$lon = $data->lon;
file_put_contents("gps.txt", "https://www.google.com/maps?q=$lat,$lon\n", FILE_APPEND);
?>
