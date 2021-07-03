<?php
require_once '/var/www/html/vendor/autoload.php';
session_start();

if (!isset($_SESSION['security_level'])) {
	$_SESSION['security_level'] = 0;
	$_SESSION['username'] = 'anonymous';
}

$loader = new \Twig\Loader\FilesystemLoader('/var/www/html/app/templates/');
$twig = new \Twig\Environment($loader, []);
echo $twig->render('index.html', []);

?>
