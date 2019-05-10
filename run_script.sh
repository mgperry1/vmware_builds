#!/bin/sh


echo "MasterNode: $1"
echo "Username: $2"
echo "Password: $3"
echo "Datastore: $4"
echo "SlaveNodes: $5"


#pwsh ./powershell_test.ps1 -SlaveNodes $5 | sed 's/[][]//g'

pwsh ./rebuild_lab_Oracle_RAC_VMDK.ps1 -MasterNode $1 -vcuser $2 -vcpass $3 -DataStore $4 -SlaveNodes $5

