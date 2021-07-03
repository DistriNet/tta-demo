<?php

require_once '/var/www/html/vendor/autoload.php';
session_start();

if (!isset($_SESSION['security_level'])) {
	$_SESSION['username'] = 'anonymous';
}

if (! isset($_GET['q'])) {
	header('Location: /');
	exit();
}

$loader = new \Twig\Loader\FilesystemLoader('/var/www/html/app/templates/');
$twig = new \Twig\Environment($loader, []);

// $dbconn = pg_connect("host=localhost dbname=vault user=vault password=UiW7V7Qw1H2Ahu");
$dbconn = pg_connect("host=db dbname=postgres user=postgres password=UiW7V7Qw1H2Ahu");
$result = pg_prepare($dbconn, "get_documents_query", 'SELECT * FROM documents WHERE content LIKE $1');
$result = pg_prepare($dbconn, "get_user_id", 'SELECT user_id, security_level FROM users WHERE name = $1');

function getAllDocuments($query) {
	global $dbconn;
	$result = pg_execute($dbconn, "get_documents_query", array("%" . $query . "%"));

	if (!$result) {
		echo "Error with query!";
		exit();
	}
	return pg_fetch_all($result);
}

function getUserSecurityLevel($username) {
	global $dbconn;
	$result = pg_execute($dbconn, "get_user_id", array($username));
	$user = pg_fetch_assoc($result);
	if (!$user) {
		echo "User does not exist...";
	}
	return $user['security_level'];
}

function filterDocuments($arr, $maxNum=10) {
	$result = [];
	foreach ($arr as $document) {
		$can_access = false;
		if ($document['min_security_level'] == 0) {
			$can_access = true;
		}
		if (getUserSecurityLevel($_SESSION['username']) >= $document['min_security_level']) {
			$can_access = true;
		}
		if ($can_access) {
			array_push($result, [
				'id' => $document["document_id"],
				'title' => $document['title'],
				'content' => substr($document['content'], 0, 500) . '...'
			]);
		}
		if (count($result) >= $maxNum) {
			break;
		}
	}
	return $result;
}

$query = $_GET['q'];
$documents = filterDocuments(getAllDocuments($query), 10);

echo $twig->render('search-results.html', 
	[
		'searchQuery' => $query,
		'documents' => $documents
	]);

?>