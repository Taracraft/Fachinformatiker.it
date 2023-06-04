<?php

$discord_url = "https://discord.com/api/oauth2/authorize?client_id= &&redirect";
header("Location: $discord_url");
exit();

?>