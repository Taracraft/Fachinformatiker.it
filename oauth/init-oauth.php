<?php

$discord_url = "https://discord.com/api/oauth2/authorize?client_id=&redirect_uri=";
header("Location: $discord_url");
exit();

?>