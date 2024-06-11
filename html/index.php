<html>
<link rel="icon" type="image/x-icon" href="favicon.ico">
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        display: flex; /* Per centrare verticalmente */
        justify-content: center; /* Per centrare orizzontalmente */
        align-items: center; /* Per centrare verticalmente */
        height: 100vh;
    }
    .container {
        display: flex;
        height: 100vh;
        height: 90%; /* Altezza della finestra */
        width: 90%; /* Larghezza della finestra */
    }
    .left-div {
        flex: 30%;
        background-color: lightgray;
        display: flex; /* Per centrare verticalmente */
        justify-content: center; /* Per centrare orizzontalmente */
        align-items: center; /* Per centrare verticalmente */
        flex-direction: column;
    }
    .right-div {
        background-color: gray;
        flex: 70%;
        display: flex; /* Per centrare verticalmente */
        justify-content: center; /* Per centrare orizzontalmente */
        align-items: center; /* Per centrare verticalmente */
    }
    .btn {
  	background-color: #6681d1;
  	color: black;
        border-radius: 15px;
  	padding: 0px 15px;
        margin: 5px 5px;
  	text-decoration: none;
    }
</style>
<title> MOBILE SENSING </title>
<body>
<div class="container">
    <div class="left-div">
      <h1> RECORDS: </h1>
      <?php
	$dir = 'records';
	$files = scandir($dir, SCANDIR_SORT_ASCENDING);
	if(count($files)>4)
	{
		$findKey = array_search('.',$files);
		unset($files[$findKey]);
        	$findKey = array_search('..',$files);
        	unset($files[$findKey]);
		$findKey = array_search('selected.json',$files);
        	unset($files[$findKey]);
		$findKey = array_search('all.json',$files);
        	unset($files[$findKey]);

		$arr_all = array();
        	foreach ($files as $file)
        	{
           		$tmp = json_decode(file_get_contents("records/".$file));
			if(!is_array($tmp))
			{
				throw new Exception("Error with File");
			}
	   		foreach($tmp as $rec)
           		{
               			array_push($arr_all, $rec);
           		}
        	}
        	$json = json_encode($arr_all);
		if(json_validate($json))
		{
			file_put_contents("records/all.json", $json);
		}
		else
		{
			throw new Exception('Error with file.');
		}

		foreach ($files as $file)
		{
  			$date = substr($file, 7, 14);
  			echo "<a  class='btn' href='index.php?file=".$file."'><h3> ".$date." </h3> </a>";
		}
        	echo "<a class='btn' href='index.php?file=all.json'><h3> ALL </h3> </a>";
	}
	else
	{
		echo "<h1>NO FILE TO SHOW</h1>";
	}
	?>
    </div>
    <div class="right-div">
	<?php
           if(isset($_GET["file"]))
	   {
		$filename = "records/".$_GET["file"];
           	if (file_exists($filename))
           	{
              		copy($filename, "records/selected.json");
			echo '<iframe src="http://192.168.1.55:3003/d-solo/cdklwcf5sehhcb/mobile-sensing?from=now&to=now-6h&orgId=1&panelId=1" width="100%" height="100%" frameborder="0"></iframe>';
		}
		else
		{
			throw new Exception('Error selecting file.');
		}
	   }
	?>
    </div>
</div>
</body>
</html>
