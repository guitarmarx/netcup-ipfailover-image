#!/bin/bash

#Erstellen des Serverfiles
if [ ! -z $SERVER_1 ]; then
		echo $SERVER_1 > /srv/servers.conf
fi		
if [ ! -z $SERVER_2 ]; then
		echo $SERVER_2 >> /srv/servers.conf
fi	
if [ ! -z $SERVER_3 ]; then
		echo $SERVER_3 >> /srv/servers.conf
fi
if [ ! -z $SERVER_4 ]; then
		echo $SERVER_4 >> /srv/servers.conf
fi
if [ ! -z $SERVER_5 ]; then
		echo $SERVER_5 >> /srv/servers.conf
fi
if [ ! -z $SERVER_6 ]; then
		echo $SERVER_6 >> /srv/servers.conf
fi
if [ ! -z $SERVER_7 ]; then
		echo $SERVER_7 >> /srv/servers.conf
fi
if [ ! -z $SERVER_8 ]; then
		echo $SERVER_8 >> /srv/servers.conf
fi
if [ ! -z $SERVER_9 ]; then
		echo $SERVER_9 >> /srv/servers.conf
fi


#Anpassen der Konfiguration
envsubst < /srv/scripts/ipfailover.py.tmpl > /srv/scripts/ipfailover.py

echo "Starting Failover script"
python /srv/scripts/ipfailover.py
