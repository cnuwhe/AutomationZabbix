
wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-1+trusty_all.deb
dpkg -i zabbix-release_3.0-1+trusty_all.deb
echo 'deb http://security.ubuntu.com/ubuntu precise-security main'>>/etc/apt/sources.list
apt-get update
apt-get install -y apache2
apt-get install -y php7
apt-get install -y php-xml
apt-get install -y php-mbstring
apt-get install -y php-bcmath
apt-get install -y mysql-server
apt-get install libmysqlclient18
apt-get install -y zabbix-server-mysql
apt-get install -y zabbix-frontend-php
apt-get install -y zabbix-agent
sed -i 's/# php_value date.timezone/php_value date.timezone/' /etc/apache2/conf-enabled/zabbix.conf
mysql -uroot -e "create database zabbix character set utf8 collate utf8_bin"
mysql -uroot -e "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix'"
cd /usr/share/doc/zabbix-server-mysql
zcat create.sql.gz|mysql -uroot zabbix
service apache2 restart
service zabbix-server start
