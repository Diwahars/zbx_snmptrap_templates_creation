## Scripts to take DB Dump for `postgres` and `mysql` specific to `zabbix` Database.

What does the script do.

1. Take backup of the database `zabbix`, given by variable `BASE='zabbix'`
2. Archive the backup and Remove old backups. 

Here is the script flow.

Create a directory if it does not exsist, this will run only once for the first time.

    # Check if directory exsists.
    if [ ! -d $BACKUP_DIR ];
    then
        mkdir -p $BACKUP_DIR
    fi

If the directory was created successfully, then take backup.     
    
    # Check if directory exsists.
    if [ -d $BACKUP_DIR ];
    then
        # Take a DB backup
        backup_postgres_db
    
        # Creating Archives.
        create_archive
    fi

## Setting up the scripts in `postgres`.

Logon to the server and `su` to `postgres` user. `$HOME` for `postgres` user is `/var/lib/pgsql`. 

1. Create/Copy the postgres script to this location `/var/lib/pgsql`.
2. Change permission to execute `chmod 777 /var/lib/pgsql/zabbix_db_backup_postgres.sh`
3. Create a directory for the backup. Similar as `/zabbix_db_backup/postgres_complete_backup/`.
4. Set owner to `postgres` which will be running the script for `backup` location in step 3.
5. Update script with new path `BACKUP_DIR=/zabbix_db_backup/postgres_complete_backup/`
6. Update script with database username `USERDB='zabbix'`, database password `PASSWD='zabbix'`,database name `BASE='zabbix'`
7. Create a file called `.pgpass`. To have the script run without the password, we need to have the `.pgpass` file in the $HOME of the `postgres` user. Format of the file is a below. (`:` seperated values)


    <postgres_server_ip>:<postgres_port>:<db_name>:<db_user>:<db_user_password>

Example: one database in one line. (Set file permissions to 0600)
    
    localhost:5432:zabbix_db_name:zabbix_user_name:zabbix_password

### Here are the command output.

    [Zubair.ahmed@nms2 /]$ sudo su postgres
    [sudo] password for Zubair.ahmed:
    bash-4.1$ pwd
    /
    bash-4.1$ cd ~
    bash-4.1$ pwd
    /var/lib/pgsql
    bash-4.1$ ls -la
    total 36
    drwx------.  3 postgres postgres 4096 Jan  6 00:27 .
    drwxr-xr-x. 43 root     root     4096 Jan  5 03:09 ..
    drwx------.  4 postgres postgres 4096 Oct  6 20:42 9.4
    -rw-------.  1 postgres postgres 1690 Jan  6 00:27 .bash_history
    -rwx------.  1 postgres postgres  267 Nov 30 16:12 .bash_profile
    -rw-------   1 postgres postgres   38 Dec 17 00:01 .pgpass
    -rw-------.  1 postgres postgres  547 Dec 17 00:23 .psql_history
    -rw-------   1 postgres postgres 3100 Jan  6 00:27 .viminfo
    -rwxrwxrwx   1 postgres postgres 2186 Jan  5 23:19 zabbix_db_backup_postgres.sh
    bash-4.1$

Here is how the `.pgpass` file looks like.
    
    bash-4.1$ cat .pgpass
    localhost:5432:zabbix:zabbix:VeryD!f1cultPassw0rd
    bash-4.1$
    
### Update crontab `postgres`

Updating the crontab with below command.

    bash-4.1$ crontab -e
    
Update the crontab with below contents.
    
    # Crontab information on how it works.
    # +----------------> minute (0 - 59)
    # |  +-------------> hour (0 - 23)
    # |  |  +----------> day of month (1 - 31)
    # |  |  |  +-------> month (1 - 12)
    # |  |  |  |  +----> day of week (0 - 6) (Sunday=0 or 7)
    # |  |  |  |  |
    # *  *  *  *  *  command to be executed

    # Execute backuo of Zabbix Database Every Week.
    0 0 * * * /var/lib/pgsql/zabbix_db_backup_postgres.sh
        
Script will run everyday at 00:00 hrs, and keeps backup for 3days.
       
## Setting up the scripts in `mysql`.       


1. Create/Copy the postgres script to user home location `$HOME`.
2. Change permission to execute `chmod 777 $HOME/zabbix_db_backup_postgres.sh`
3. Create a directory for the backup. Similar as `/zabbix_db_backup/postgres_complete_backup/`.
4. Set owner to the `user` which will be running the script for `backup` location in step 3.
5. Update script with new path `BACKUP_DIR=/zabbix_db_backup/postgres_complete_backup/`
6. Update script with database username `USERDB='zabbix'`, database password `PASSWD='zabbix'`,database name `BASE='zabbix'`

### Update crontab `mysql`

Updating the crontab with below command.

    crontab -e
    
Update the crontab with below contents.
    
    # Crontab information on how it works.
    # +----------------> minute (0 - 59)
    # |  +-------------> hour (0 - 23)
    # |  |  +----------> day of month (1 - 31)
    # |  |  |  +-------> month (1 - 12)
    # |  |  |  |  +----> day of week (0 - 6) (Sunday=0 or 7)
    # |  |  |  |  |
    # *  *  *  *  *  command to be executed

    # Execute backuo of Zabbix Database Every Week.
    0 0 * * * /var/lib/pgsql/zabbix_db_backup_mysql.sh

Script will run everyday at 00:00 hrs, and keeps backup for 3days.