<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

if(!isset($_GET['code'])){
    echo 'Keine Daten';
    exit();
}
$discord_code = $_GET['code'];

//Config
$bot_token = "";
$payload = [
    'code'=>$discord_code,
    'client_id'=>'',
    'client_secret'=>'',
/////////////////////////////////////////////////////////////////////////////
//Ab Hier nichts verändern                                                 //
////////////////////////////////////////////////////////////////////////////
    'grant_type'=>'authorization_code',
    'redirect_uri'=>'https://auth.fachinformatik.it/process-oauth.php',
    'scope'=>'identify%20guids',
];


//API zusammen Bauen

//print_r($payload);
$payload_string = http_build_query($payload);
$discord_token_url = "https://discordapp.com/api/oauth2/token";
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $discord_token_url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload_string);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
$result = curl_exec($ch);
if(!$result){
    echo curl_error($ch);
}
$result = json_decode($result,true);
$access_token = $result['access_token'];
$discord_users_url = "https://discordapp.com/api/users/@me";
$header = array("Authorization: Bearer $access_token", "Content-Type: application/x-www-form-urlencoded");
$ch = curl_init();
curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
curl_setopt($ch, CURLOPT_URL, $discord_users_url);
curl_setopt($ch, CURLOPT_POST, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
$result = curl_exec($ch);
$result = json_decode($result, true);
$guildobject = getGuildObject($access_token, '1089909008867012701');
$guild_roles = $guildobject['roles'];
// see if roles has the correct role_id within the array

$role = 'user';
if(in_array('1089909009269653544', $guild_roles)){
    $role = 'Admins';
}else if(in_array('1092170908413743134', $guild_roles)){
    $role = 'Moderator';
}

//Funktionen

function addUserToGuild($discord_ID,$token,$guild_ID){
    $payload = [
        'access_token'=>$token,
    ];
    $discord_api_url = 'https://discordapp.com/api/guilds/'.$guild_ID.'/members/'.$discord_ID;
    $header = array("Authorization: Bot $bot_token", "Content-Type: application/json");

    $ch = curl_init();
    //set the url, number of POST vars, POST data
    curl_setopt($ch, CURLOPT_HTTPHEADER,$header);
    curl_setopt($ch,CURLOPT_URL, $discord_api_url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT"); //must be put for this method..
    curl_setopt($ch,CURLOPT_POSTFIELDS, json_encode($payload)); //must be a json body
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);

    $result = curl_exec($ch);

    if(!$result){
        echo curl_error($ch);
    }else{
        return true;
    }
}

function getGuildObject($access_token, $guild_id){
    //requires the following scope: guilds.members.read
    $discord_api_url = "https://discordapp.com/api";
    $header = array("Authorization: Bearer $access_token","Content-Type: application/x-www-form-urlencoded");
    $ch = curl_init();
    //set the url, number of POST vars, POST data
    curl_setopt($ch, CURLOPT_HTTPHEADER,$header);
    curl_setopt($ch,CURLOPT_URL, $discord_api_url.'/users/@me/guilds/'.$guild_id.'/member');
    curl_setopt($ch,CURLOPT_POST, false);
    //curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    $result = curl_exec($ch);
    $result = json_decode($result,true);
    return $result;
}


//Benutzer zum server Hinzufuegen
$guild_ID = '1089909008867012701';
$addUserToGuild = addUserToGuild($result['id'],$access_token,$guild_ID);

// Rollen Check
if($role=='Admins'){
    header("location: admin/admin-lounge.php");
}else if($role=='Moderator'){
    header("location: admin/moderator-lounge.php");
}else{
    header("location: dashboard.php");
}

//Start
session_start();

$_SESSION['logged_in'] = true;
$_SESSION['userData'] = [
    'name'=>$result['username'],
    'discord_id'=>$result['id'],
    'avatar'=>$result['avatar'],
    'role' =>$role,
];

exit();
?>