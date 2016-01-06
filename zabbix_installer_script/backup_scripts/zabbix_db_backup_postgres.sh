#!/bin/sh

# !!!!!! IMPORTANT !!!!!! 
#
# To have the script run without the password,
# we need to have the `.pgpass` file in the $HOME of the `postgres` user.
#
# Format of the file is a below. (`:` seperated values)
# 
# <postgres_server_ip>:<postgres_port>:<db_name>:<db_user>:<db_user_password>
# 
# Example: one database in one line. (Set file permissions to 0600)
# localhost:5432:zabbix_db_name:zabbix_user_name:zabbix_password
#


USERDB='zabbix'
BASE='zabbix'

USER='postgres'
NMS_SERVER_NAME=`uname -n | cut -d'-' -f1`


BACKUP_DIR=/tmp/backup_zabbix_db
DATE=`date "+%Y_%m_%d_%H_%M"`
PREV=`date -d '7 days ago' "+%Y_%m_%d"`

FILE_NAME=${NMS_SERVER_NAME}_DBBACKUP_${DATE}.dump
FILE_NAME_TGZ=${FILE_NAME}.tgz


backup_postgres_db()
{
	# -------------------
	# Example Commands
	# -------------------
	
		# Passing `--file` to store the file.
		#
		#  sudo -u postgres pg_dump --host localhost --port 5432 \
		#  			--username zabbix --format custom --blobs --verbos \
		#			--file /tmp/backup_db/zbx.dump zabbix

		
		#  Redirecting file using `>`.
		#
		#  sudo -u postgres pg_dump --host localhost --port 5432 \
		#  			--username zabbix --format custom --blobs --verbos \
		#			zabbix > /tmp/backup_db/zbx.dump zabbix

	# ----------------
	# TAKING BACKUP
	# ----------------
	
	/usr/bin/pg_dump --host localhost --port 5432 \
		--username $USERDB --format custom --blobs --verbos \
		--file ${BACKUP_DIR}/${FILE_NAME} ${BASE}
		
}


start_service()
{
    # Start Zabbix Server.
    echo "Backup Complete - Starting Server Services."
    service zabbix-server start
    service zabbix-server status
}

create_archive()
{
    cd $BACKUP_DIR

    echo "Creating Archive."
    tar cvzf ${FILE_NAME_TGZ} ${FILE_NAME}

    echo "Changing owner to user from root."
    chown $USER:$USER ${FILE_NAME}.tgz

    echo "Removing Unarchived Backup."
    rm $BACKUP_DIR/${FILE_NAME}

    echo "Removing Archives older than 7 days."
    rm $BACKUP_DIR/${NMS_SERVER_NAME}_DBBACKUP_$PREV*

    cd -
}


# Check if directory exsists.
if [ ! -d $BACKUP_DIR ];
then
    mkdir -p $BACKUP_DIR
fi

# Check if directory exsists.
if [ -d $BACKUP_DIR ];
then
    # Take a DB backup
    backup_postgres_db

    # Creating Archives.
    create_archive
fi


