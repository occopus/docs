$db_name = hiera("dbname")
$db_user = hiera("dbuser")
$db_pass = hiera("dbpass")
$db_host = hiera("mysqlhost")

class { 'apache':
  disableboot => false
}

apache::module { 'php5':
   install_package => 'libapache2-mod-php5',
}

class { 'php': }
php::module { 'mysql': }

class { 'wordpress':
  db_name     => "$db_name",
  db_user        => "$db_user",
  db_password    => "$db_pass",
  create_db      => false,
  create_db_user => false,
  install_dir => '/var/www/html/wordpress',
  db_host => "$db_host"
}
