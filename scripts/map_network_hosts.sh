#!/bin/bash
###############################################################
#
#This is a bash script to execute the Django management command
# for capturing the SNMP status of all the hosts withing the
# specified network and map hostname with ip addresses
# for registered locations.
#
#Usage: Ideally this script shall be scheduled as a CRON job
#to be executed repetitively after a particular time interval.
#(Eg. Everyday at 11pm)
#
###############################################################

LOGGINS_PATH_TO_ENV=''
#Example: LOGGINS_PATH_TO_ENV = '/home/darshan/projects/loggins/ENV'
LOGGINS_PROJECT_DIR=''
#Example: LOGGINS_INSTALL_DIR = '/home/darshan/projects/loggins/loggins'
NETWORK_PREFIXES=''
#Enter multiple network prefixes separated by a single space
#Example:
#NETWORK_PREFIXES='192.168.1'
#or
#NETWORK_PREFIXES='192.168.1 10.0.0'

if [ "$LOGGINS_PATH_TO_ENV" == "" ]; then
    echo "Please configure the path to virtual environment under Loggins application"
    exit 1
fi

if [ "$LOGGINS_PROJECT_DIR" == "" ]; then
    echo "Please configure the path to project directory of Loggins application"
    exit 1
fi

if [ "$NETWORK_PREFIXES" == "" ]; then
    echo "Please enter valid network prefixes separated by a single space"
    exit 1
fi

source $LOGGINS_PATH_TO_ENV/bin/activate
echo "-----------Activated virtual environment-----------------"
cd $LOGGINS_PROJECT_DIR
echo "----Executing management command 'map_network_hosts'----"
python manage.py map_network_hosts $NETWORK_PREFIXES
deactivate
echo "----------Deactivated virtual environment----------------"
