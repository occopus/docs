$mysql_password = hiera("rootpassword")
$db_name = hiera("dbname")
$db_user = hiera("dbuser")
$db_pass = hiera("dbpass")
$db_access = "%.%.%.%"

class { '::mysql::server':
  root_password    => $mysql_password,
  override_options => { 'mysqld' => { 'bind-address' => '0.0.0.0' } }
}

mysql::db { $db_name:
  user     => $db_user,
  password => $db_pass,
  host     => $db_access,
  grant  => 'ALL',
}
