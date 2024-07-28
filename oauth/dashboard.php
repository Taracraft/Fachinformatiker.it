<?php
session_start();

if (!$_SESSION['logged_in']) {
    header('Location: error.php');
    exit();
}

extract($_SESSION['userData']);

$avatar_url = "https://cdn.discordapp.com/avatars/$discord_id/$avatar.png";
$display_name = ucfirst(strtolower($name));
?>
<!doctype html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <link href="style/css/output.css" rel="stylesheet">
    <link href="style/css/styles.css" rel="stylesheet">
    <title>Dashboard</title>
</head>
<body class="bg-discord-gray flex flex-col items-center justify-center min-h-screen">
    <div class="main-container flex">
        <div class="additional-boxes">
            <div class="box">
                <h2>Box 1</h2>
                <p>Beispieltext für Box 1.</p>
            </div>
            <div class="box">
                <h2>Box 2</h2>
                <p>Beispieltext für Box 2.</p>
            </div>
            <div class="box">
                <h2>Box 3</h2>
                <p>Beispieltext für Box 3.</p>
            </div>
            <div class="box">
                <h2>Box 4</h2>
                <p>Beispieltext für Box 4.</p>
            </div>
        </div>
        <div class="container mx-4">
            <div class="header">
                <div class="avatar-container">
                    <img class="w-12 h-12" src="<?php echo htmlspecialchars($avatar_url); ?>" alt="Avatar">
                    <h1 class="text-4xl font-bold text-white ml-4"><?php echo htmlspecialchars($display_name); ?></h1>
                </div>
                <div class="text-white text-3xl mt-2">Willkommen zum Dashboard</div>
            </div>

            <div class="content">
                <div class="text-white text-3xl mt-4">Cloud-Zugang:</div>
                <div class="cloud-link mt-4">
                    <a href="https://cloud.fachinformatik.it/" target="_blank">
                        <img src="images/logo.png" alt="Cloud Logo" height="200" width="200">
                    </a>
                </div>
            </div>

            <div class="footer mt-6">
                <a href="logout.php" class="text-gray-300">Logout</a>
            </div>
        </div>
        <div class="additional-boxes">
            <div class="box">
                <h2>Box 5</h2>
                <p>Beispieltext für Box 5.</p>
            </div>
            <div class="box">
                <h2>Box 6</h2>
                <p>Beispieltext für Box 6.</p>
            </div>
            <div class="box">
                <h2>Box 7</h2>
                <p>Beispieltext für Box 7.</p>
            </div>
            <div class="box">
                <h2>Box 8</h2>
                <p>Beispieltext für Box 8.</p>
            </div>
        </div>
    </div>
</body>
</html>

