#!/bin/bash
#Shell script to capture Mac state:logged-out. See http://github.com/gwu-libraries/loggins for more information.

#Determine workstation ethernet adapter IP address
IP=$(ifconfig en0 | grep inet | grep -v inet6 | awk '{ print $2}') 

#Set API connection information
API_KEY=
API_USERNAME=
API_URL=

#Send CURL command to API
curl -i -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: ApiKey $API_USERNAME:$API_KEY" -X PUT -d "{\"ip_address\":\"$IP\",\"state\":\"a\",\"observation_time\":\"$(date +%Y-%m-%dT%H:%M:%S)\"}" $API_URL

#ECHO CURL command for debugging
echo curl -i -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: ApiKey $API_USERNAME:$API_KEY" -X PUT -d "{\"ip_address\":\"$IP\",\"state\":\"a\",\"observation_time\":\"$(date +%Y-%m-%dT%H:%M:%S)\"}" $API_URL
