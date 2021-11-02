
Ricezione dati da ESP8266 </br> 
<?php
$dati=file_get_contents('php://input');
$temperature = json_decode(file_get_contents('php://input'));

/*
$Terra=htmlspecialchars($_GET["terra"]);
$mezza=htmlspecialchars($_GET["mezza"]);
$alto=htmlspecialchars($_GET["alto"]);

echo 'terra ' . htmlspecialchars($_GET["terra"]) . ' gradi</br>' ;
echo 'mezza ' . htmlspecialchars($_GET["mezza"]) . ' gradi</br>';
echo 'alto ' . htmlspecialchars($_GET["alto"]) . ' gradi</br>';
*/
echo 'terra ' . $temperature->terra . ' gradi</br>' ;
echo 'mezza ' . $temperature->mezza . ' gradi</br>';
echo 'alto ' .  $temperature->alto  . ' gradi</br>';


?>

<?php
//    file_put_contents("dati",$Terra .',' . $mezza . ',' . $alto);
    file_put_contents("dati",$dati);

?>