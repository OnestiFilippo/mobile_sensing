<?php declare(strict_types=1);

use PHPUnit\Framework\TestCase;

function json_validate(string $json): bool {
    json_decode($json);
    return (json_last_error() === JSON_ERROR_NONE);
}

final class FileClass
{
    public function createAllArray($files)
    {
            //$dir = '../html/records';
            //$files = scandir($dir, SCANDIR_SORT_ASCENDING);
            $arr_all = array();
            foreach ($files as $file)
            {
		    $tmp = json_decode(file_get_contents("testrecords/".$file));
		    if(!is_array($tmp))
		    {
		    	throw new Exception("Error with file");
                    }

		    foreach($tmp as $rec)
                    {
                            array_push($arr_all, $rec);
                    }
            }
            $json = json_encode($arr_all);
            if(json_validate($json))
            {
                    //file_put_contents("records/all.json", $json);
                    return true;
            }
            else
            {
                    throw new Exception('Error with file');
            }
    }

    public function selectFile($file)
    {
	        $filename = "testrecords/".$file;
                if (file_exists($filename))
                {
                        copy($filename, "testrecords/selected.json");
                        //echo '<iframe src="http://192.168.1.55:3003/d-solo/cdklwcf5sehhcb/mobile-sensing?from=now&to=now-6h&orgId=1&panelId=1" width="100%" height="100%">
			return true;
                }
                else
                {
                        throw new Exception('Error selecting file.');
                }
    }
}

final class FileClassTest extends TestCase
{
    public function testCreateAllArrayTrue(): void
    {
        $fileclass = new FileClass;

	$fixture = array(
                        0 => "record_dd-mm-yy_hh-mm.json"
                        );

        $res = $fileclass->createAllArray($fixture);

        $this->assertTrue($res);
    }

    public function testCreateAllArrayFileFail(): void
    {
        $fileclass = new FileClass;

        $fixture = array(
                        0 => "record_dd-mm-yy_hh-mm_E.json"
                        );

	$this->expectException(Exception::class);

        $res = $fileclass->createAllArray($fixture);
    }

    public function testSelectFileTrue(): void
    {
        $fileclass = new FileClass;

        $file = "record_dd-mm-yy_hh-mm.json";

        $res = $fileclass->selectFile($file);

        $this->assertTrue($res);
    }

    public function testSelectFileFail(): void
    {
        $fileclass = new FileClass;

        $file = "record_dd-mm-yy_hh-mmA.json";

        $this->expectException(Exception::class);

        $res = $fileclass->selectFile($file);
    }
}
