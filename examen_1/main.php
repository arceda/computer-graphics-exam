<?php
//echo shell_exec('env') ;
	
header("Access-Control-Allow-Origin: *");
date_default_timezone_set('America/Lima');

try {

    $cui        =  $_POST["cui"];	
    $question   =  $_POST["question"];	
    $code       =  $_POST["code"];	

    $path = "/var/www/html/computer-graphics-exam/examen_1/exams/$cui";
    //$path = "/home/vicente/exams/$cui";
    //$path_2 = "/var/www/html/computer-graphics/examen_1/exams/$cui/$question";

    if (!file_exists($path)) {
        mkdir($path, 0777, true);
    }

    //if (!file_exists($path_2)) {
    //    mkdir($path_2, 0777, true);
    //}

    $fp = fopen("$path/$question.py", 'w');
    fwrite($fp, "#".date("M-d-Y h:i:s A")."\n");
    fwrite($fp, $code);
    fclose($fp);

    $response = array('code_result' => 1, 'message' => "Envio exitoso");
    echo json_encode($response);

} catch (Exception $e) {
    $response = array('code_result' => 0, 'message' => $response);
    echo json_encode($response);
}


?>