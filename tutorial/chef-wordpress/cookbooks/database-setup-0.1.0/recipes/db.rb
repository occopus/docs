#
# Cookbook Name:: wordpress-app
# Recipe:: default
#
# Copyright 2014, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

include_recipe "mysql::server"
include_recipe "database::mysql"

mysql_database 'wordpress' do
  database_name node['database_management']['database_name']
  connection(
    :host     => 'localhost',
    :username => 'root',
    :password => node['mysql']['server_root_password']
  )
  action :create
end

mysql_database_user 'wordpress_user' do
  username node['database_management']['dbuser_username']
  connection(
    :host     => 'localhost',
    :username => 'root',
    :password => node['mysql']['server_root_password']
  )
  password node['database_management']['dbuser_password']
  database_name node['database_management']['database_name']
  host '%'
  privileges [:select, :update, :insert, :create, :delete]
  action     :grant
end

