#!/bin/sh

USERDB='zabbix'
PASSWD='zabbix'
BASE='zabbix'

USER='globetouch'
NMS_SERVER_NAME=`uname -n | cut -d'-' -f1`


BACKUP_DIR=/home/${USER}/backup_zabbix_db
DATE=`date "+%Y_%m_%d_%H_%M"`
PREV=`date -d '7 days ago' "+%Y_%m_%d"`

FILE_NAME=${NMS_SERVER_NAME}_DBBACKUP_${DATE}.sql
FILE_NAME_TGZ=${FILE_NAME}.tgz

backup_db()
{

    cd $BACKUP_DIR

    echo "Creating Backup - Using mysqldump."
    mysqldump -u$USERDB -p$PASSWD ${BASE} > ${FILE_NAME}

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
    backup_db

    # Creating Archives.
    create_archive
fi


