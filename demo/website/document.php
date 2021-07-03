<?php

require_once '/var/www/html/vendor/autoload.php';
session_start();

if (!isset($_SESSION['security_level'])) {
	$_SESSION['username'] = 'anonymous';
}

$loader = new \Twig\Loader\FilesystemLoader('/var/www/html/app/templates/');
$twig = new \Twig\Environment($loader, []);

// $dbconn = pg_connect("host=localhost dbname=vault user=vault password=UiW7V7Qw1H2Ahu");
$dbconn = pg_connect("host=db dbname=postgres user=postgres password=UiW7V7Qw1H2Ahu");
$result = pg_prepare($dbconn, "get_document_by_id", 'SELECT * FROM documents WHERE document_id = $1');

function getDocument($id) {
	global $dbconn;
	$result = pg_execute($dbconn, "get_document_by_id", array($id));

	if (!$result) {
		echo "Error with query!";
		exit();
	}
	return pg_fetch_assoc($result);
}

$document_id = $_GET['id'];

echo $twig->render('document-view.html', 
	[
		'searchQuery' => $query,
		'document' => getDocument($document_id)
	]);

?>