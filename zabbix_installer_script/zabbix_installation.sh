#!/bin/bash

#
# Text Formating
#

BOLD="\033[1m";
NORM="\033[0m";

BLACK_F="\033[30m"; BLACK_B="\033[40m"
RED_F="\033[31m"; RED_B="\033[41m"
GREEN_F="\033[32m"; GREEN_B="\033[42m"
YELLOW_F="\033[33m"; YELLOW_B="\033[43m"
BLUE_F="\033[34m"; BLUE_B="\033[44m"
MAGENTA_F="\033[35m"; MAGENTA_B="\033[45m"
CYAN_F="\033[36m"; CYAN_B="\033[46m"
WHITE_F="\033[37m"; WHITE_B="\033[47m"

###########


function zabbix_repo()
{
	echo -e "${RED_B}${BOLD}Installing Repository. ${NORM}"
	rpm -ivh http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/zabbix-release-2.4-1.el6.noarch.rpm
}

function mysql()
{
	echo -e "${RED_B}${BOLD}Installing MYSQL Server and Client. ${NORM}"
	yum install mysql-server mysql -y

	mysql_install_status=`command -v mysql`;
	if [[ $mysql_install_status == *"mysql"* ]]
	then
		echo -e "${GREEN_F}${BOLD}mysql installed successfully. ${NORM}";
	else
		echo -e "${RED_F}${BOLD} mysql was not Installed, please verify!!! Quitting now. :( ${NORM}"
		exit
	fi
}

function net_snmp()
{
	echo -e "${RED_B}${BOLD}Installing net-snmp-utils and net-snmp-perl. ${NORM}"
	yum install -y net-snmp-utils net-snmp-perl

	net_snmp_status=`command -v snmptrap`;
	if [[ $net_snmp_status == *"snmptrap"* ]]
	then
		echo -e "${GREEN_F}${BOLD}net_snmp installed successfully. ${NORM}";
	else
		echo -e "${RED_F}${BOLD} net_snmp was not Installed, please verify!!! Aborting now. :( ${NORM}"
		exit
	fi
}

function zabbix_server_web()
{
	echo -e "${RED_B}${BOLD}Installing Zabbix Server and Web Interface. ${NORM}"
	yum install zabbix-server-mysql zabbix-web-mysql -y

	zabbix_server_mysql_status=`command -v zabbix_server_mysql`;
	if [[ $zabbix_server_mysql_status == *"zabbix_server_mysql"* ]]
	then
		echo -e "${GREEN_F}${BOLD}zabbix_server_mysql installed successfully. ${NORM}";
	else
		echo -e "${RED_F}${BOLD} zabbix_server_mysql was not Installed, please verify!!! Aborting now. :( ${NORM}"
		exit
	fi
}

function zabbix_agent()
{
	echo -e "${RED_B}${BOLD}Installing Agent. ${NORM}"
	yum install zabbix-agent -y

	zabbix_agent_status=`command -v zabbix_agent`;
	if [[ $zabbix_agent_status == *"zabbix_agent"* ]]
	then
		echo -e "${GREEN_F}${BOLD}zabbix_agent installed successfully. ${NORM}";
	else
		echo -e "${RED_F}${BOLD} zabbix_agent was not Installed, please verify!!! Aborting now. :( ${NORM}"
		exit
	fi
}

function start_mysql_server()
{
	echo -e "${CYAN_F}${BOLD} Start Mysql Server ${NORM}"

	check_if_mysql_running=`service mysqld status`
	if [[ $check_if_mysql_running == *"running"* ]]
	then
		echo -e "${GREEN_F}${BOLD}mysql server started. ${NORM}";
	else
		echo "Starting MYSQL Server"
		service mysqld start

	fi
}

function create_zabbix_db()
{
	echo -e "${CYAN_F}${BOLD} Creating zabbix Database, if it does not exists. ${NORM}"
	echo "create database if not exists zabbix character set utf8 collate utf8_bin;" | mysql -u root 
	echo "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';" | mysql -u root
}

function create_zabbix_schema()
{

	version_string_complete=`zabbix_server --version | head -1  |  cut -d' ' -f3`; 
	version=${version_string_complete:1}

	echo -e "${RED_F}${BOLD} Zabbix Version Running : $version ${NORM}"

	if [ ! -f /usr/share/doc/zabbix-server-mysql-${version}/create/schema.sql ];
	then
		echo -e "${RED_F}${BOLD} Could not find schema.sql file quitting now. ${NORM}"
		exit
	fi

	table_count=`echo "use zabbix; show tables;" | mysql -uroot | wc -l`
	if [[ $table_count == '0' ]]
	then
		echo -e "${YELLOW_F}${BOLD}Adding zabbix DB with schema.sql ${NORM}"
		mysql -uroot zabbix < /usr/share/doc/zabbix-server-mysql-${version}/create/schema.sql

		echo -e "${YELLOW_F}${BOLD}Adding zabbix DB with image.sql ${NORM}"
		mysql -uroot zabbix < /usr/share/doc/zabbix-server-mysql-${version}/create/images.sql

		echo -e "${YELLOW_F}${BOLD}Adding zabbix DB with data.sql ${NORM}"
		mysql -uroot zabbix < /usr/share/doc/zabbix-server-mysql-${version}/create/data.sql
	else
		echo -e "${RED_F}${BOLD} Tables already exists, skipping this task. ${NORM}"
	fi
	
}

function zabbix_server_config()
{
	if [ -f /etc/zabbix/zabbix_server.conf ];
	then 
		cp /etc/zabbix/zabbix_server.conf /etc/zabbix/zabbix_server.conf.org
		echo -e "${CYAN_F}${BOLD} Updating zabbix_server.conf ${NORM}"
		echo -e "

# Logging Information	
LogFile=/var/log/zabbix/zabbix_server.log
LogFileSize=0

# PID File Information
PidFile=/var/run/zabbix/zabbix_server.pid

# Database related information
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=zabbix

# Mysql SOCKET
DBSocket=/var/lib/mysql/mysql.sock

# Trap file information, for snmptt.
#SNMPTrapperFile=/var/log/snmptt/snmptt.log
SNMPTrapperFile=/tmp/zabbix_traps.tmp

# Enable SNMP Trapper
StartSNMPTrapper=1

# Script path.
AlertScriptsPath=/usr/lib/zabbix/alertscripts
ExternalScripts=/usr/lib/zabbix/externalscripts

	" > /etc/zabbix/zabbix_server.conf

	else
		echo -e "${RED_F}${BOLD} File zabbix_server.conf not found, please check zabbix-server installation. ${NORM}"
		exit
	fi

}


function start_zabbix_server()
{
	echo -e "${CYAN_F}${BOLD} Start Zabbix Server ${NORM}"
	service zabbix-server start

	check_if_server_running=`service zabbix-server status`
	if [[ $check_if_server_running == *"running"* ]]
	then
		echo -e "${GREEN_F}${BOLD}zabbix server started ${NORM}";
	else
		echo -e "${RED_F}${BOLD} Zabbix Server Could not start - Aborting. ${NORM}"
		exit
	fi
}

function update_web_settings()
{
	echo -e "${CYAN_F}${BOLD} Update Web settings. ${NORM}"

	if [ -f /etc/httpd/conf.d/zabbix.conf ];
	then
		mv /etc/httpd/conf.d/zabbix.conf /etc/httpd/conf.d/zabbix.conf.org
		echo -e "#
# Zabbix monitoring system php web frontend
#

Alias /zabbix /usr/share/zabbix

<Directory \"/usr/share/zabbix\">
	Options FollowSymLinks
	AllowOverride None
	Order allow,deny
	Allow from all

	<IfModule mod_php5.c>
		php_value max_execution_time 300
		php_value memory_limit 128M
		php_value post_max_size 16M
		php_value upload_max_filesize 5M
		php_value max_input_time 300
		php_value date.timezone Asia/Kolkata
	</IfModule>
</Directory>

<Directory \"/usr/share/zabbix/conf\">
	Order deny,allow
	Deny from all
	<files *.php>
		Order deny,allow
		Deny from all
	</files>
</Directory>

<Directory \"/usr/share/zabbix/api\">
	Order deny,allow
	Deny from all
	<files *.php>
		Order deny,allow
		Deny from all
	</files>
</Directory>

<Directory \"/usr/share/zabbix/include\">
	Order deny,allow
	Deny from all
	<files *.php>
		Order deny,allow
		Deny from all
	</files>
</Directory>

<Directory \"/usr/share/zabbix/include/classes\">
	Order deny,allow
	Deny from all
	<files *.php>
		Order deny,allow
		Deny from all
	</files>
</Directory>
" > /etc/httpd/conf.d/zabbix.conf

	else
		echo -e "${RED_F}${BOLD} File zabbix.conf not found, please check zabbix-web installation.${NORM}"
		exit
	fi
}

function create_perl_trap_recv()
{
	if [ -f /usr/bin/zabbix_trap_receiver.pl ];
	then
		echo -e "${RED_F}${BOLD} /usr/bin/zabbix_trap_receiver.pl Already present skipping.${NORM}"
	else
	
		echo -e "${CYAN_F}${BOLD} Creating File in /usr/bin/zabbix_trap_receiver.pl. ${NORM}"
		
		if [ -f zabbix_trap_receiver.pl ];
		then
			echo -e "${CYAN_F}${BOLD} Copy File to /usr/bin/zabbix_trap_receiver.pl ${NORM}" 
			cp zabbix_trap_receiver.pl /usr/bin/zabbix_trap_receiver.pl
			
			echo -e "${CYAN_F}${BOLD} setting execute permissions to perl file. ${NORM}"
			chmod +x /usr/bin/zabbix_trap_receiver.pl
		
		else
			echo -e "${CYAN_F}${BOLD} File was not present in the current directory, Downloading from github. ${NORM}"
			wget https://raw.githubusercontent.com/miraclelinux/MIRACLE-ZBX-2.0.3-NoSQL/master/misc/snmptrap/zabbix_trap_receiver.pl
			
			echo -e "${CYAN_F}${BOLD} Copy File to /usr/bin/zabbix_trap_receiver.pl ${NORM}" 
			cp zabbix_trap_receiver.pl /usr/bin/zabbix_trap_receiver.pl
			
			echo -e "${CYAN_F}${BOLD} setting execute permissions to perl file. ${NORM}"
			chmod +x /usr/bin/zabbix_trap_receiver.pl
		fi	
	
	fi
}

function updating_snmptrapd_config()
{
	echo -e "${CYAN_F}${BOLD} Updating snmptrapd.conf file. ${NORM}"
	echo -e "# Example configuration file for snmptrapd
#
# No traps are handled by default, you must edit this file!
#
# authCommunity   log,execute,net public
# traphandle SNMPv2-MIB::coldStart    /usr/bin/bin/my_great_script cold

authCommunity execute public 
perl do \"/usr/bin/zabbix_trap_receiver.pl\";
" > /etc/snmp/snmptrapd.conf

}

function start_httpd()
{
	echo -e "${GREEN_F}${BOLD}Starting httpd service. ${NORM}"
	service httpd start
}

function start_up_services()
{
	echo -e "${GREEN_F}${BOLD}Setting startup application. ${NORM}"
	chkconfig httpd on
	chkconfig iptables off
	chkconfig zabbix-agent on
	chkconfig zabbix-server on
	chkconfig mysqld on
	chkconfig snmpd on
	chkconfig snmptrapd on
}

function create_directory_for_rollover()
{
	echo -e "${CYAN_F}${BOLD} Creating directory to archive trap logs. ${NORM}"
	mkdir -p /var/log/zabbix_traps_archive
	chmod 777 /var/log/zabbix_traps_archive
}

function create_logrotate_snmptraps()
{
	echo -e "${CYAN_F}${BOLD} Creating file /etc/logrotate.d/zabbix_traps for trap logs. ${NORM}"
	echo -e "/tmp/zabbix_traps.tmp {
    weekly
    size 10M
    compress
    compresscmd /usr/bin/bzip2
    compressoptions -9
    notifempty
    dateext
    dateformat -%Y%m%d
    missingok
    olddir /var/log/zabbix_traps_archive
    maxage 365
    rotate 10
}" > /etc/logrotate.d/zabbix_traps

}

zabbix_repo
mysql
net_snmp
zabbix_server_web
zabbix_agent
start_mysql_server
create_zabbix_db
create_zabbix_schema
zabbix_server_config
start_zabbix_server
update_web_settings
create_perl_trap_recv
updating_snmptrapd_config
start_httpd
create_directory_for_rollover
create_logrotate_snmptraps
start_up_services
service zabbix-server restart
service snmptrapd restart