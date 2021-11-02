
<!DOCTYPE html>
<html>
<head>
<title>Visualizza dati</title>
</head>
<body>

<h1>Dati </h1>
<p> Dati <script>Date(); </script> </p>

<?php
    $temperature=json_decode(file_get_contents('dati'));
//    echo $dati->  . "<br>";
    echo 'terra ' . $temperature->terra . ' gradi</br>' ;
    echo 'mezza ' . $temperature->mezza . ' gradi</br>';
    echo 'alto ' .  $temperature->alto  . ' gradi</br>';


?>

</body>
</html>