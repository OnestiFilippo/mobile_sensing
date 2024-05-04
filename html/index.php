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
        height: 80%; /* Altezza della finestra */
        width: 80%; /* Larghezza della finestra */
    }
    .left-div {
        flex: 30%;
        background-color: lightblue;
        display: flex; /* Per centrare verticalmente */
        justify-content: center; /* Per centrare orizzontalmente */
        align-items: center; /* Per centrare verticalmente */
        flex-direction: column;
    }
    .right-div {
        flex: 70%;
        background-color: lightgreen;
        display: flex; /* Per centrare verticalmente */
        justify-content: center; /* Per centrare orizzontalmente */
        align-items: center; /* Per centrare verticalmente */
    }
</style>
<title> MOBILE SENSING </title>
<body>
<div class="container">
    <div class="left-div">
      <?php

	$dir    = 'records';
	$files = scandir($dir, SCANDIR_SORT_ASCENDING);

 	$dim = count($files);
	unset($files[0]);
	unset($files[1]);
	unset($files[$dim-1]);

	foreach ($files as $file)
	{
  		$date = substr($file, 7, 16);
  		echo "<a href='filippoonesti.ovh:83/index.php?".$date."'><h2> ".$date." </h2> </a>";
	}
	?>
    </div>
    <div class="right-div">
            <iframe src="http://192.168.1.55:3003/d-solo/cdklwcf5sehhcb/mobile-sensing?from=now&to=now-6h&orgId=1&panelId=1" width="1400" height="700" frameborder="0"></iframe>
    </div>
</div>
</body>
</html>
