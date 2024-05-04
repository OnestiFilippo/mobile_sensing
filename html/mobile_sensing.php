<?php

$jsonData = file_get_contents('php://input');
// Decode the JSON data into a PHP associative array
$data = json_decode($jsonData, true);
// Check if decoding was successful
if ($data !== null) {
   $dim = count($data);
   $filename = $data[$dim-1]['name'];
   unset($data[$dim-1]);
   $jsonData = json_encode($data);
   $file = 'records/'.$filename;
   file_put_contents($file, $jsonData);
} else {
   // JSON decoding failed
   http_response_code(400); // Bad Request
   echo "Invalid JSON data";
}
?>
