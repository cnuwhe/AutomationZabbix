#! bin/sh
wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-1+trusty_all.deb
dpkg -i zabbix-release_3.0-1+trusty_all.deb
apt-get update
apt-get install -y zabbix-server-mysql 
apt-get install zabbix-frontend-php
apt-get install zabbix-agent
cd /usr/share/doc/zabbix-server-mysql
zcat create.sql.gz | mysql -uroot zabbix
# vi /etc/zabbix/zabbix_server.conf
#DBHost=localhost
#DBName=zabbix
#DBUser=zabbix
#DBPassword=zabbix
service zabbix-server start