<?php
session_start();

if(!$_SESSION['logged_in']){
  header('Location: error.php');
  exit();
}
extract($_SESSION['userData']);

$avatar_url = "https://cdn.discordapp.com/avatars/$discord_id/$avatar.png";
$guilds = $_SESSION['userData']['guilds'];
$guildMarkup='';

foreach ($guilds as $key => $guildData) {
    $guildMarkup.='<li class="py-2 px-4 w-full rounded-t-lg border-b border-gray-200 dark:border-gray-600">'.$guildData['name'].'</li>';
}
?>
<!doctype html>
<html lang="">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="css/output.css" rel="stylesheet">
    <title></title>
</head>
<body>
    <div class="flex items-center justify-center h-screen bg-discord-gray flex-col">
      <div class="text-white text-3xl">Willkommen zum Dashboard, </div>
      <div class="flex items-center mt-4">
        <img class="rounded-full w-12 h-12 mr-3" src="<?php echo $avatar_url?>"  alt=""/>
        <span class="text-3xl text-white font-semibold"><?php echo $name;?></span>
        <ul class="w-96 text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 dark:bg-gray-700 dark:border-gray-600 dark:text-white mt-6">
           <h3 class="text-xl font-bold ml-3 text-gray-300 uppercase py-2">Discord-Server:</h3>
           <?php echo $guildMarkup;?>
      </ul>
      </div>
        <div class="text-white text-3xl">Cloud-Zugang:
        <a href="https://cloud.fachinformatik.it/cloud/" target="_blank"><img src="img/logo.png" alt="" height="200" width="200"></img></div></a>
        <a href="logout.php" class="mt-5 text-gray-300">Logout</a>
    </div>

</body>
</html>



</html>