<?php declare(strict_types=1);

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
                    throw new Exception('Error writing all.json file.');
            }
    }
}
