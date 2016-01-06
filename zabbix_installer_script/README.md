## Zabbix Installation on Centos/Redhat 6.x

Scripts does 2 Major installations.

1. Setting up basic zabbix installation.
2. Setup zabbix trapper using perl script.

### Here is what the script does at a lower level.

1. Installing `zabbix` Repo.
2. Install `mysql`.
3. Install `net_snmp`, this is used for the `snmp_trapper` which we install later on.
4. Install `zabbix` Server and Web interface.
5. Install `zabbix` Agent.
6. Starting `mysql` and create `zabbix` default schema.
7. Configuration of `zabbix` server.
8. Update web settings with timezone and upload file limit.
9. Setting up `perl` snmp trapper script.
10. Update `snmptrapd` configuration.
11. Setting up logrotation for `zabbix snmp trapper`, Creating directory to store archived logs.
12. `diable` selinux and reboot the server.


### Here is an extract from the script.

    echo -e "${YELLOW_B}${BOLD} ####### INSTALL ZABBIX REPO. ####### ${NORM}"
    zabbix_repo
    
    echo -e "${YELLOW_B}${BOLD} ###### INSTALL MYSQL. ###### ${NORM}"
    install_mysql
    
    echo -e "${YELLOW_B}${BOLD} ###### INSTALL NET_SNMP. ###### ${NORM}"
    net_snmp
    
    echo -e "${YELLOW_B}${BOLD} ###### INSTALL ZABBIX SERVER AND WEB. ###### ${NORM}"
    zabbix_server_web
    
    echo -e "${YELLOW_B}${BOLD} ###### INSTALL ZABBIX AGENT. ###### ${NORM}"
    zabbix_agent
    
    echo -e "${YELLOW_B}${BOLD} ###### STARTING MYSQL SERVER. ###### ${NORM}"
    start_mysql_server
    
    echo -e "${YELLOW_B}${BOLD} ###### CREATING ZABBIX DATABASE. ###### ${NORM}"
    create_zabbix_db
    
    echo -e "${YELLOW_B}${BOLD} ###### POPULATING DEFAULT SCHEMA. ###### ${NORM}"
    create_zabbix_schema
    
    echo -e "${YELLOW_B}${BOLD} ###### CONFIGURING ZABBIX SERVER. ###### ${NORM}"
    zabbix_server_config
    
    echo -e "${YELLOW_B}${BOLD} ###### STARTING ZABBIX SERVER. ###### ${NORM}"
    start_zabbix_server
    
    echo -e "${YELLOW_B}${BOLD} ###### UPDATING WEB SETTINGS. ###### ${NORM}"
    update_web_settings
    
    echo -e "${YELLOW_B}${BOLD} ###### CREATING PERL TRAPPER. ###### ${NORM}"
    create_perl_trap_recv
    
    echo -e "${YELLOW_B}${BOLD} ###### UPDATE SNMPTRAPD CONFIG. ###### ${NORM}"
    updating_snmptrapd_config
    
    echo -e "${YELLOW_B}${BOLD} ###### STARTING HTTPD ###### ${NORM}"
    start_httpd
    
    echo -e "${YELLOW_B}${BOLD} ###### INSTALL ZABBIX REPO ###### ${NORM}"
    create_directory_for_rollover
    
    echo -e "${YELLOW_B}${BOLD} ###### CREATING LOGROTATE FOR SNMPTRAPS. ###### ${NORM}"
    create_logrotate_snmptraps
    
    echo -e "${YELLOW_B}${BOLD} ###### SETTING START UP SERVICES. ###### ${NORM}"
    start_up_services
    
    echo -e "${YELLOW_B}${BOLD} ###### RESTART ZABBIX-SERVER ###### ${NORM}"
    service zabbix-server restart
    
    echo -e "${YELLOW_B}${BOLD} ###### RESTART SNMPTRAPD. ###### ${NORM}"
    service snmptrapd restart
    
    echo -e "${YELLOW_B}${BOLD} ###### DISABLE SELINUX. ###### ${NORM}"
    setting_selinux_config
    
    echo -e "${CYAN_F}${BOLD} ###### REBOOTING SERVER. ###### ${NORM}"
    reboot

Once the server reboot got to below link and complete the installation.

	http://localhost/zabbix

Default username/password `Admin/zabbix`.


## Here is the command output.

Executing the script.

If there is any issue the script will exit.

	[root@localhost Downloads]# sh zbx_install.sh
	 ####### INSTALL ZABBIX REPO. #######
	Installing Repository.
	Retrieving http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/zabbix-release-2.4-1.el6.noarch.rpm
	warning: /var/tmp/rpm-tmp.G2uE1q: Header V4 DSA/SHA1 Signature, key ID 79ea5ed4: NOKEY
	Preparing...                ########################################### [100%]
	   1:zabbix-release         ########################################### [100%]
	 ###### INSTALL MYSQL. ######
	Installing MYSQL Server and Client.
	Loaded plugins: fastestmirror, refresh-packagekit, security
	Setting up Install Process
	Determining fastest mirrors
	epel/metalink                                                                                                    | 5.2 kB     00:00
	 * base: mirror.nbrc.ac.in
	 * epel: ftp.riken.jp
	 * extras: mirror.nbrc.ac.in
	 * updates: mirror.nbrc.ac.in
	base                                                                                                             | 3.7 kB     00:00
	base/primary_db                                                                                                  | 4.6 MB     00:02
	epel                                                                                                             | 4.3 kB     00:00
	epel/primary_db                                                                                                  | 5.7 MB     00:02
	extras                                                                                                           | 2.9 kB     00:00
	extras/primary_db                                                                                                |  33 kB     00:00
	updates                                                                                                          | 3.4 kB     00:00
	updates/primary_db                                                                                               | 3.3 MB     00:01
	http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/repodata/repomd.xml: [Errno 12] Timeout on http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/repodata/repomd.xml: (28, 'Operation too slow. Less than 1 bytes/sec transfered the last 30 seconds')
	Trying other mirror.
	Error: Cannot retrieve repository metadata (repomd.xml) for repository: zabbix. Please verify its path and try again
	 mysql was not Installed, please verify!!! Quitting now. :(

Here more successful installation. 

	[root@localhost Downloads]# sh zbx_install.sh
	 ####### INSTALL ZABBIX REPO. #######
	Installing Repository.
	Retrieving http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/zabbix-release-2.4-1.el6.noarch.rpm
	warning: /var/tmp/rpm-tmp.7HT5LS: Header V4 DSA/SHA1 Signature, key ID 79ea5ed4: NOKEY
	Preparing...                ########################################### [100%]
	        package zabbix-release-2.4-1.el6.noarch is already installed
	 ###### INSTALL MYSQL. ######
	Installing MYSQL Server and Client.
	Loaded plugins: fastestmirror, refresh-packagekit, security
	Setting up Install Process
	Loading mirror speeds from cached hostfile
	 * base: mirror.nbrc.ac.in
	 * epel: ftp.riken.jp
	 * extras: mirror.nbrc.ac.in
	 * updates: mirror.nbrc.ac.in
	zabbix                                                                                                           |  951 B     00:00
	zabbix/primary                                                                                                   |  23 kB     00:00
	zabbix                                                                                                                          145/145
	zabbix-non-supported                                                                                             |  951 B     00:00
	zabbix-non-supported/primary                                                                                     | 3.8 kB     00:00
	zabbix-non-supported                                                                                                              15/15
	Resolving Dependencies
	--> Running transaction check
	---> Package mysql.x86_64 0:5.1.73-5.el6_6 will be installed
	--> Processing Dependency: mysql-libs = 5.1.73-5.el6_6 for package: mysql-5.1.73-5.el6_6.x86_64
	---> Package mysql-server.x86_64 0:5.1.73-5.el6_6 will be installed
	--> Processing Dependency: perl-DBI for package: mysql-server-5.1.73-5.el6_6.x86_64
	--> Processing Dependency: perl-DBD-MySQL for package: mysql-server-5.1.73-5.el6_6.x86_64
	--> Processing Dependency: perl(DBI) for package: mysql-server-5.1.73-5.el6_6.x86_64
	--> Running transaction check
	---> Package mysql-libs.x86_64 0:5.1.73-3.el6_5 will be updated
	---> Package mysql-libs.x86_64 0:5.1.73-5.el6_6 will be an update
	---> Package perl-DBD-MySQL.x86_64 0:4.013-3.el6 will be installed
	---> Package perl-DBI.x86_64 0:1.609-4.el6 will be installed
	--> Finished Dependency Resolution
	
	Dependencies Resolved
	
	========================================================================================================================================
	 Package                             Arch                        Version                                Repository                 Size
	========================================================================================================================================
	Installing:
	 mysql                               x86_64                      5.1.73-5.el6_6                         base                      894 k
	 mysql-server                        x86_64                      5.1.73-5.el6_6                         base                      8.6 M
	Installing for dependencies:
	 perl-DBD-MySQL                      x86_64                      4.013-3.el6                            base                      134 k
	 perl-DBI                            x86_64                      1.609-4.el6                            base                      705 k
	Updating for dependencies:
	 mysql-libs                          x86_64                      5.1.73-5.el6_6                         base                      1.2 M
	
	Transaction Summary
	========================================================================================================================================
	Install       4 Package(s)
	Upgrade       1 Package(s)
	
	Total download size: 12 M
	Downloading Packages:
	(1/5): mysql-5.1.73-5.el6_6.x86_64.rpm                                                                           | 894 kB     00:01
	(2/5): mysql-libs-5.1.73-5.el6_6.x86_64.rpm                                                                      | 1.2 MB     00:02
	(3/5): mysql-server-5.1.73-5.el6_6.x86_64.rpm                                                                    | 8.6 MB     00:12
	(4/5): perl-DBD-MySQL-4.013-3.el6.x86_64.rpm                                                                     | 134 kB     00:03
	(5/5): perl-DBI-1.609-4.el6.x86_64.rpm                                                                           | 705 kB     00:01
	----------------------------------------------------------------------------------------------------------------------------------------
	Total                                                                                                   316 kB/s |  12 MB     00:37
	Running rpm_check_debug
	Running Transaction Test
	Transaction Test Succeeded
	Running Transaction
	Warning: RPMDB altered outside of yum.
	  Updating   : mysql-libs-5.1.73-5.el6_6.x86_64                                                                                     1/6
	  Installing : perl-DBI-1.609-4.el6.x86_64                                                                                          2/6
	  Installing : perl-DBD-MySQL-4.013-3.el6.x86_64                                                                                    3/6
	  Installing : mysql-5.1.73-5.el6_6.x86_64                                                                                          4/6
	  Installing : mysql-server-5.1.73-5.el6_6.x86_64                                                                                   5/6
	  Cleanup    : mysql-libs-5.1.73-3.el6_5.x86_64                                                                                     6/6
	  Verifying  : mysql-libs-5.1.73-5.el6_6.x86_64                                                                                     1/6
	  Verifying  : mysql-5.1.73-5.el6_6.x86_64                                                                                          2/6
	  Verifying  : mysql-server-5.1.73-5.el6_6.x86_64                                                                                   3/6
	  Verifying  : perl-DBI-1.609-4.el6.x86_64                                                                                          4/6
	  Verifying  : perl-DBD-MySQL-4.013-3.el6.x86_64                                                                                    5/6
	  Verifying  : mysql-libs-5.1.73-3.el6_5.x86_64                                                                                     6/6
	
	Installed:
	  mysql.x86_64 0:5.1.73-5.el6_6                                   mysql-server.x86_64 0:5.1.73-5.el6_6
	
	Dependency Installed:
	  perl-DBD-MySQL.x86_64 0:4.013-3.el6                                   perl-DBI.x86_64 0:1.609-4.el6
	
	Dependency Updated:
	  mysql-libs.x86_64 0:5.1.73-5.el6_6
	
	Complete!
	mysql installed successfully.
	 ###### INSTALL NET_SNMP. ######
	Installing net-snmp-utils and net-snmp-perl.
	Loaded plugins: fastestmirror, refresh-packagekit, security
	Setting up Install Process
	Loading mirror speeds from cached hostfile
	 * base: mirror.nbrc.ac.in
	 * epel: ftp.riken.jp
	 * extras: mirror.nbrc.ac.in
	 * updates: mirror.nbrc.ac.in
	Resolving Dependencies
	--> Running transaction check
	---> Package net-snmp-perl.x86_64 1:5.5-54.el6_7.1 will be installed
	--> Processing Dependency: net-snmp-libs = 1:5.5-54.el6_7.1 for package: 1:net-snmp-perl-5.5-54.el6_7.1.x86_64
	---> Package net-snmp-utils.x86_64 1:5.5-54.el6_7.1 will be installed
	--> Running transaction check
	---> Package net-snmp-libs.x86_64 1:5.5-49.el6_5.3 will be updated
	--> Processing Dependency: net-snmp-libs = 1:5.5-49.el6_5.3 for package: 1:net-snmp-5.5-49.el6_5.3.x86_64
	---> Package net-snmp-libs.x86_64 1:5.5-54.el6_7.1 will be an update
	--> Running transaction check
	---> Package net-snmp.x86_64 1:5.5-49.el6_5.3 will be updated
	---> Package net-snmp.x86_64 1:5.5-54.el6_7.1 will be an update
	--> Finished Dependency Resolution
	
	Dependencies Resolved
	
	========================================================================================================================================
	 Package                            Arch                       Version                                Repository                   Size
	========================================================================================================================================
	Installing:
	 net-snmp-perl                      x86_64                     1:5.5-54.el6_7.1                       updates                     324 k
	 net-snmp-utils                     x86_64                     1:5.5-54.el6_7.1                       updates                     176 k
	Updating for dependencies:
	 net-snmp                           x86_64                     1:5.5-54.el6_7.1                       updates                     308 k
	 net-snmp-libs                      x86_64                     1:5.5-54.el6_7.1                       updates                     1.5 M
	
	Transaction Summary
	========================================================================================================================================
	Install       2 Package(s)
	Upgrade       2 Package(s)
	
	Total download size: 2.3 M
	Downloading Packages:
	(1/4): net-snmp-5.5-54.el6_7.1.x86_64.rpm                                                                        | 308 kB     00:00
	(2/4): net-snmp-libs-5.5-54.el6_7.1.x86_64.rpm                                                                   | 1.5 MB     00:00
	(3/4): net-snmp-perl-5.5-54.el6_7.1.x86_64.rpm                                                                   | 324 kB     00:01
	(4/4): net-snmp-utils-5.5-54.el6_7.1.x86_64.rpm                                                                  | 176 kB     00:00
	----------------------------------------------------------------------------------------------------------------------------------------
	Total                                                                                                   403 kB/s | 2.3 MB     00:05
	Running rpm_check_debug
	Running Transaction Test
	Transaction Test Succeeded
	Running Transaction
	  Updating   : 1:net-snmp-libs-5.5-54.el6_7.1.x86_64                                                                                1/6
	  Installing : 1:net-snmp-utils-5.5-54.el6_7.1.x86_64                                                                               2/6
	  Installing : 1:net-snmp-perl-5.5-54.el6_7.1.x86_64                                                                                3/6
	  Updating   : 1:net-snmp-5.5-54.el6_7.1.x86_64                                                                                     4/6
	  Cleanup    : 1:net-snmp-5.5-49.el6_5.3.x86_64                                                                                     5/6
	  Cleanup    : 1:net-snmp-libs-5.5-49.el6_5.3.x86_64                                                                                6/6
	  Verifying  : 1:net-snmp-libs-5.5-54.el6_7.1.x86_64                                                                                1/6
	  Verifying  : 1:net-snmp-utils-5.5-54.el6_7.1.x86_64                                                                               2/6
	  Verifying  : 1:net-snmp-perl-5.5-54.el6_7.1.x86_64                                                                                3/6
	  Verifying  : 1:net-snmp-5.5-54.el6_7.1.x86_64                                                                                     4/6
	  Verifying  : 1:net-snmp-libs-5.5-49.el6_5.3.x86_64                                                                                5/6
	  Verifying  : 1:net-snmp-5.5-49.el6_5.3.x86_64                                                                                     6/6
	
	Installed:
	  net-snmp-perl.x86_64 1:5.5-54.el6_7.1                              net-snmp-utils.x86_64 1:5.5-54.el6_7.1
	
	Dependency Updated:
	  net-snmp.x86_64 1:5.5-54.el6_7.1                                 net-snmp-libs.x86_64 1:5.5-54.el6_7.1
	
	Complete!
	net_snmp installed successfully.
	 ###### INSTALL ZABBIX SERVER AND WEB. ######
	Installing Zabbix Server and Web Interface.
	Loaded plugins: fastestmirror, refresh-packagekit, security
	Setting up Install Process
	Loading mirror speeds from cached hostfile
	 * base: mirror.nbrc.ac.in
	 * epel: ftp.riken.jp
	 * extras: mirror.nbrc.ac.in
	 * updates: mirror.nbrc.ac.in
	Resolving Dependencies
	--> Running transaction check
	---> Package zabbix-server-mysql.x86_64 0:2.4.7-1.el6 will be installed
	--> Processing Dependency: zabbix-server = 2.4.7-1.el6 for package: zabbix-server-mysql-2.4.7-1.el6.x86_64
	--> Processing Dependency: libiksemel.so.3()(64bit) for package: zabbix-server-mysql-2.4.7-1.el6.x86_64
	--> Processing Dependency: libOpenIPMIposix.so.0()(64bit) for package: zabbix-server-mysql-2.4.7-1.el6.x86_64
	--> Processing Dependency: libodbc.so.2()(64bit) for package: zabbix-server-mysql-2.4.7-1.el6.x86_64
	--> Processing Dependency: libOpenIPMI.so.0()(64bit) for package: zabbix-server-mysql-2.4.7-1.el6.x86_64
	---> Package zabbix-web-mysql.noarch 0:2.4.7-1.el6 will be installed
	--> Processing Dependency: zabbix-web = 2.4.7-1.el6 for package: zabbix-web-mysql-2.4.7-1.el6.noarch
	--> Processing Dependency: php-mysql for package: zabbix-web-mysql-2.4.7-1.el6.noarch
	--> Running transaction check
	---> Package OpenIPMI-libs.x86_64 0:2.0.16-14.el6 will be installed
	---> Package iksemel.x86_64 0:1.4-2.el6 will be installed
	---> Package php-mysql.x86_64 0:5.3.3-46.el6_6 will be installed
	--> Processing Dependency: php-common(x86-64) = 5.3.3-46.el6_6 for package: php-mysql-5.3.3-46.el6_6.x86_64
	--> Processing Dependency: php-pdo(x86-64) for package: php-mysql-5.3.3-46.el6_6.x86_64
	---> Package unixODBC.x86_64 0:2.2.14-14.el6 will be installed
	---> Package zabbix-server.x86_64 0:2.4.7-1.el6 will be installed
	--> Processing Dependency: zabbix for package: zabbix-server-2.4.7-1.el6.x86_64
	--> Processing Dependency: fping for package: zabbix-server-2.4.7-1.el6.x86_64
	---> Package zabbix-web.noarch 0:2.4.7-1.el6 will be installed
	--> Processing Dependency: php >= 5.3 for package: zabbix-web-2.4.7-1.el6.noarch
	--> Processing Dependency: php-gd for package: zabbix-web-2.4.7-1.el6.noarch
	--> Processing Dependency: php-mbstring for package: zabbix-web-2.4.7-1.el6.noarch
	--> Processing Dependency: php-bcmath for package: zabbix-web-2.4.7-1.el6.noarch
	--> Processing Dependency: php-xml for package: zabbix-web-2.4.7-1.el6.noarch
	--> Running transaction check
	---> Package fping.x86_64 0:2.4b2-16.el6 will be installed
	---> Package php.x86_64 0:5.3.3-46.el6_6 will be installed
	--> Processing Dependency: php-cli(x86-64) = 5.3.3-46.el6_6 for package: php-5.3.3-46.el6_6.x86_64
	---> Package php-bcmath.x86_64 0:5.3.3-46.el6_6 will be installed
	---> Package php-common.x86_64 0:5.3.3-46.el6_6 will be installed
	---> Package php-gd.x86_64 0:5.3.3-46.el6_6 will be installed
	--> Processing Dependency: libXpm.so.4()(64bit) for package: php-gd-5.3.3-46.el6_6.x86_64
	---> Package php-mbstring.x86_64 0:5.3.3-46.el6_6 will be installed
	---> Package php-pdo.x86_64 0:5.3.3-46.el6_6 will be installed
	---> Package php-xml.x86_64 0:5.3.3-46.el6_6 will be installed
	---> Package zabbix.x86_64 0:2.4.7-1.el6 will be installed
	--> Running transaction check
	---> Package libXpm.x86_64 0:3.5.10-2.el6 will be installed
	---> Package php-cli.x86_64 0:5.3.3-46.el6_6 will be installed
	--> Finished Dependency Resolution
	
	Dependencies Resolved
	
	========================================================================================================================================
	 Package                             Arch                   Version                          Repository                            Size
	========================================================================================================================================
	Installing:
	 zabbix-server-mysql                 x86_64                 2.4.7-1.el6                      zabbix                               1.5 M
	 zabbix-web-mysql                    noarch                 2.4.7-1.el6                      zabbix                                15 k
	Installing for dependencies:
	 OpenIPMI-libs                       x86_64                 2.0.16-14.el6                    base                                 473 k
	...
	 php-xml                             x86_64                 5.3.3-46.el6_6                   updates                              107 k
	 unixODBC                            x86_64                 2.2.14-14.el6                    base                                 378 k
	 zabbix                              x86_64                 2.4.7-1.el6                      zabbix                               163 k
	 zabbix-server                       x86_64                 2.4.7-1.el6                      zabbix                                22 k
	 zabbix-web                          noarch                 2.4.7-1.el6                      zabbix                               4.5 M
	
	Transaction Summary
	========================================================================================================================================
	Install      19 Package(s)
	
	Total download size: 12 M
	Installed size: 50 M
	Downloading Packages:
	(1/19): OpenIPMI-libs-2.0.16-14.el6.x86_64.rpm                                                                   | 473 kB     00:00
	....
	(15/19): zabbix-2.4.7-1.el6.x86_64.rpm                                                                           | 163 kB     00:00
	(16/19): zabbix-server-2.4.7-1.el6.x86_64.rpm                                                                    |  22 kB     00:00
	(17/19): zabbix-server-mysql-2.4.7-1.el6.x86_64.rpm                                                              | 1.5 MB     00:01
	(18/19): zabbix-web-2.4.7-1.el6.noarch.rpm                                                                       | 4.5 MB     00:00
	(19/19): zabbix-web-mysql-2.4.7-1.el6.noarch.rpm                                                                 |  15 kB     00:00
	----------------------------------------------------------------------------------------------------------------------------------------
	Total                                                                                                   295 kB/s |  12 MB     00:41
	warning: rpmts_HdrFromFdno: Header V4 DSA/SHA1 Signature, key ID 79ea5ed4: NOKEY
	Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-ZABBIX
	Importing GPG key 0x79EA5ED4:
	 Userid : Zabbix SIA <packager@zabbix.com>
	 Package: zabbix-release-2.4-1.el6.noarch (installed)
	 From   : /etc/pki/rpm-gpg/RPM-GPG-KEY-ZABBIX
	Running rpm_check_debug
	Running Transaction Test
	Transaction Test Succeeded
	Running Transaction
	  Installing : php-common-5.3.3-46.el6_6.x86_64                                                                                    1/19
	  Installing : unixODBC-2.2.14-14.el6.x86_64                                                                                       2/19
	  Installing : OpenIPMI-libs-2.0.16-14.el6.x86_64                                                                                  3/19
	  Installing : iksemel-1.4-2.el6.x86_64                                                                                            4/19
	  Installing : php-xml-5.3.3-46.el6_6.x86_64                                                                                       5/19
	  Installing : php-pdo-5.3.3-46.el6_6.x86_64                                                                                       6/19
	  Installing : php-mysql-5.3.3-46.el6_6.x86_64                                                                                     7/19
	....
	  Verifying  : fping-2.4b2-16.el6.x86_64                                                                                          19/19
	
	Installed:
	  zabbix-server-mysql.x86_64 0:2.4.7-1.el6                             zabbix-web-mysql.noarch 0:2.4.7-1.el6
	
	Dependency Installed:
	  OpenIPMI-libs.x86_64 0:2.0.16-14.el6          fping.x86_64 0:2.4b2-16.el6                 iksemel.x86_64 0:1.4-2.el6
	  libXpm.x86_64 0:3.5.10-2.el6                  php.x86_64 0:5.3.3-46.el6_6                 php-bcmath.x86_64 0:5.3.3-46.el6_6
	  php-cli.x86_64 0:5.3.3-46.el6_6               php-common.x86_64 0:5.3.3-46.el6_6          php-gd.x86_64 0:5.3.3-46.el6_6
	  php-mbstring.x86_64 0:5.3.3-46.el6_6          php-mysql.x86_64 0:5.3.3-46.el6_6           php-pdo.x86_64 0:5.3.3-46.el6_6
	  php-xml.x86_64 0:5.3.3-46.el6_6               unixODBC.x86_64 0:2.2.14-14.el6             zabbix.x86_64 0:2.4.7-1.el6
	  zabbix-server.x86_64 0:2.4.7-1.el6            zabbix-web.noarch 0:2.4.7-1.el6
	
	Complete!
	zabbix_server_mysql installed successfully.
	 ###### INSTALL ZABBIX AGENT. ######
	Installing Agent.
	Loaded plugins: fastestmirror, refresh-packagekit, security
	Setting up Install Process
	Loading mirror speeds from cached hostfile
	 * base: mirror.nbrc.ac.in
	 * epel: ftp.riken.jp
	 * extras: mirror.nbrc.ac.in
	 * updates: mirror.nbrc.ac.in
	Resolving Dependencies
	--> Running transaction check
	---> Package zabbix-agent.x86_64 0:2.4.7-1.el6 will be installed
	--> Finished Dependency Resolution
	
	Dependencies Resolved
	
	========================================================================================================================================
	 Package                            Arch                         Version                             Repository                    Size
	========================================================================================================================================
	Installing:
	 zabbix-agent                       x86_64                       2.4.7-1.el6                         zabbix                       173 k
	
	Transaction Summary
	========================================================================================================================================
	Install       1 Package(s)
	
	Total download size: 173 k
	Installed size: 557 k
	Downloading Packages:
	zabbix-agent-2.4.7-1.el6.x86_64.rpm                                                                              | 173 kB     00:00
	Running rpm_check_debug
	Running Transaction Test
	Transaction Test Succeeded
	Running Transaction
	  Installing : zabbix-agent-2.4.7-1.el6.x86_64                                                                                      1/1
	  Verifying  : zabbix-agent-2.4.7-1.el6.x86_64                                                                                      1/1
	
	Installed:
	  zabbix-agent.x86_64 0:2.4.7-1.el6
	
	Complete!
	zabbix_agent installed successfully.
	 ###### STARTING MYSQL SERVER. ######
	 Start Mysql Server
	Starting MYSQL Server
	Initializing MySQL database:  Installing MySQL system tables...
	OK
	Filling help tables...
	OK
	
	To start mysqld at boot time you have to copy
	support-files/mysql.server to the right place for your system
	
	PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
	To do so, start the server, then issue the following commands:
	
	/usr/bin/mysqladmin -u root password 'new-password'
	/usr/bin/mysqladmin -u root -h localhost.localdomain password 'new-password'
	
	Alternatively you can run:
	/usr/bin/mysql_secure_installation
	
	which will also give you the option of removing the test
	databases and anonymous user created by default.  This is
	strongly recommended for production servers.
	
	See the manual for more instructions.
	
	You can start the MySQL daemon with:
	cd /usr ; /usr/bin/mysqld_safe &
	
	You can test the MySQL daemon with mysql-test-run.pl
	cd /usr/mysql-test ; perl mysql-test-run.pl
	
	Please report any problems with the /usr/bin/mysqlbug script!
	
	                                                           [  OK  ]
	Starting mysqld:                                           [  OK  ]
	 ###### CREATING ZABBIX DATABASE. ######
	 Creating zabbix Database, if it does not exists.
	 ###### POPULATING DEFAULT SCHEMA. ######
	 Zabbix Version Running : 2.4.7
	Adding zabbix DB with schema.sql
	Adding zabbix DB with image.sql
	Adding zabbix DB with data.sql
	 ###### CONFIGURING ZABBIX SERVER. ######
	 Updating zabbix_server.conf
	 ###### STARTING ZABBIX SERVER. ######
	 Start Zabbix Server
	Starting Zabbix server:                                    [  OK  ]
	zabbix server started
	 ###### UPDATING WEB SETTINGS. ######
	 Update Web settings.
	 ###### CREATING PERL TRAPPER. ######
	 Creating File in /usr/bin/zabbix_trap_receiver.pl.
	 File was not present in the current directory, Downloading from github.
	--2016-01-06 02:11:37--  https://raw.githubusercontent.com/miraclelinux/MIRACLE-ZBX-2.0.3-NoSQL/master/misc/snmptrap/zabbix_trap_receiver.pl
	Resolving raw.githubusercontent.com... 103.245.222.133
	Connecting to raw.githubusercontent.com|103.245.222.133|:443... connected.
	HTTP request sent, awaiting response... 200 OK
	Length: 3611 (3.5K) [text/plain]
	Saving to: “zabbix_trap_receiver.pl”
	
	100%[==============================================================================================>] 3,611       --.-K/s   in 0s
	
	2016-01-06 02:11:43 (97.8 MB/s) - “zabbix_trap_receiver.pl” saved [3611/3611]
	
	 Copy File to /usr/bin/zabbix_trap_receiver.pl
	 setting execute permissions to perl file.
	 ###### UPDATE SNMPTRAPD CONFIG. ######
	 Updating snmptrapd.conf file.
	 ###### STARTING HTTPD ######
	Starting httpd service.
	Starting httpd: httpd: Could not reliably determine the server's fully qualified domain name, using localhost.localdomain for ServerName
	                                                           [  OK  ]
	 ###### INSTALL ZABBIX REPO ######
	 Creating directory to archive trap logs.
	 ###### CREATING LOGROTATE FOR SNMPTRAPS. ######
	 Creating file /etc/logrotate.d/zabbix_traps for trap logs.
	 ###### SETTING START UP SERVICES. ######
	Setting startup application.
	 ###### RESTART ZABBIX-SERVER ######
	Shutting down Zabbix server:                               [  OK  ]
	Starting Zabbix server:                                    [  OK  ]
	 ###### RESTART SNMPTRAPD. ######
	Stopping snmptrapd:                                        [FAILED]
	Starting snmptrapd: Loaded Zabbix SNMP trap receiver
	                                                           [  OK  ]
	 ###### DISABLE SELINUX. ######
	 Taking current configuration backup.
	 Disabling SELINUX.
	 ###### REBOOTING SERVER. ######
	
	Broadcast message from ahmed@localhost.localdomain
	        (/dev/pts/2) at 2:11 ...
	
	The system is going down for reboot NOW!
	[root@localhost Downloads]#


### Next step after running the script.

Goto browser `http://localhost/zabbix`

![Screen 1](http://zubayr.github.io/images/zabbix_install_1.jpg)

Check settings. All are green.

![Screen 2](http://zubayr.github.io/images/zabbix_install_2.jpg)

Enter mysql credentials. 

![Screen 3](http://zubayr.github.io/images/zabbix_install_3.jpg)

Enter server name. 

![Screen 4](http://zubayr.github.io/images/zabbix_install_4.jpg)

Check details.

![Screen 5](http://zubayr.github.io/images/zabbix_install_5.jpg)

Installation complete  (Almost).

![Screen 6](http://zubayr.github.io/images/zabbix_install_6.jpg)

Logon to server, default username/password. (Admin/zabbix)

![Screen 7](http://zubayr.github.io/images/zabbix_install_7.jpg)

Dashboard. Installation Complete.

![Screen 8](http://zubayr.github.io/images/zabbix_install_8.jpg)

Checking backend `perl` trapper.

![Screen 8](http://zubayr.github.io/images/zabbix_install_9.jpg)