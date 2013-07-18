#!/bin/bash
###############################################################
#
#This is a bash script to execute the Django management command
# for capturing the SNMP status of all the registered locations
# in the Loggins application.
#
#Usage: Ideally this script shall be scheduled as a CRON job
#to be executed repetitively after a particular time interval.
#(Eg. After every 30 seconds)
#
###############################################################

LOGGINS_PATH_TO_ENV=''
#Example: LOGGINS_PATH_TO_ENV = '/home/darshan/projects/loggins/ENV'
LOGGINS_PROJECT_DIR=''
#Example: LOGGINS_INSTALL_DIR = '/home/darshan/projects/loggins/loggins'

if [ "$LOGGINS_PATH_TO_ENV" == "" ]; then
    echo "Please configure the path to virual environment under Loggins application"
    exit 1
fi

if [ "$LOGGINS_PROJECT_DIR" == "" ]; then
    echo "Please configure the path to project directory of Loggins application"
    exit 1
fi

source $LOGGINS_PATH_TO_ENV/bin/activate
echo "-----------Activated virtual environment-----------------"
cd $LOGGINS_PROJECT_DIR
echo "----Executing management command 'capture_snmp_state'----"
python manage.py capture_snmp_state
deactivate
echo "----------Deactivated virtual environment----------------"
