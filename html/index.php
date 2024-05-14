<?php
	if(isset($_GET["file"]))
	{
		$filename = "records/".$_GET["file"];
                copy($filename, "records/selected.json");
	}
?>
<html>
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
</style>
<title> MOBILE SENSING </title>
<body>
<div class="container">
    <div class="left-div">
      <h1> RECORDS: </h1>
      <?php
	$dir    = 'records';
	$files = scandir($dir, SCANDIR_SORT_ASCENDING);

 	$dim = count($files);
	unset($files[0]);
	unset($files[1]);
	unset($files[$dim-1]);

	foreach ($files as $file)
	{
  		$date = substr($file, 7, 14);
  		echo "<a href='index.php?file=".$file."'><h3> ".$date." </h3> </a>";
	}
	?>
    </div>
    <div class="right-div">
	<?php
           if(isset($_GET["file"]))
	   {
		echo '<iframe src="http://192.168.1.55:3003/d-solo/cdklwcf5sehhcb/mobile-sensing?from=now&to=now-6h&orgId=1&panelId=1" width="100%" height="100%" frameborder="0"></iframe>';
	   }
	?>
    </div>
</div>
</body>
</html>
