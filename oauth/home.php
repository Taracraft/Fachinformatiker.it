<?
// We need to use sessions, so you should always start sessions using the below code.
session_start();
// If the user is not logged in redirect to the login page...
if (!isset($_SESSION['loggedin'])) {
    header('Location: ../../cms/index.html');
	exit;
}
include("style/template/header.php");
include("style/template/nav.php");
?>
<div class="content">
<h2>Home Bereich</h2>
<p>Willkommen Zur&uumlck <?=$_SESSION['name']?>!</p>
</div>
<?
include("style/template/footer.php");
?>