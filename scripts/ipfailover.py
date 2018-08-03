import logging
import subprocess
import os
import requests
import re
import time
from modules.netcupapi import NetcupAPI
from modules import helper
from modules.server import Server


#####     PARAMETER     #####
smtpServer = os.environ["SMTP_SERVER"]
smtpPort = os.environ["SMTP_PORT"]
smtpUser = os.environ["SMTP_USER"]
smtpPass = os.environ["SMTP_PASS"]
smtpSourceMail = os.environ["SMTP_SOURCE_MAIL"]
smtpTargetMail = os.environ["SMTP_TARGET_MAIL"]

netcupUser = os.environ["NETCUP_USER"]
netcupPassword = os.environ["NETCUP_PASSWORD"]
netcupAPIUrl = os.environ["NETCUP_API_URL"]
failoverIP = os.environ["FAILOVER_IP"]
failoverIPNetmask = os.environ["FAILOVER_NETMASK"]

timeBetweenPings = os.environ["TIME_BETWEEN_PINGS"]
messages = helper.getMessages("messages.ini")
logFile = '/srv/failover.log'
logFormat = '%(asctime)s - %(levelname)s - %(message)s'

# read failover server
failoverServers = helper.getFailoverServers()
for failoverServer in failoverServers:
    failoverServer.printInfos()

# create netcupAPI object
netcupAPI = NetcupAPI(netcupAPIUrl, netcupUser, netcupPassword,
                      failoverIP, failoverIPNetmask)


def getCurrentIPFailoverServer():
    for failoverServer in failoverServers:
        # check if server has failover ip
        if netcupAPI.hasServerFailoverIP(failoverServer):
            return failoverServer


def getFirstPingableServer():
    for failoverServer in failoverServers:
        if failoverServer.isPingable():
            return failoverServer



# ----------------MAIN----------------------------
failoverErrorOccured = False

# Init Logger
logger = helper.initLogging(logFormat, logFile)
logger.info("script started ...")

while True:

    if not helper.isFailoverIPPingable(failoverIP, timeBetweenPings):
        # Start Failover
        # get server with failoverIP
        logger.info('Starting failover...')

        currentFailoverIPServer = getCurrentIPFailoverServer()
        logger.info('Current failover server: ' + currentFailoverIPServer.name)

        # delete IP Routing
        if netcupAPI.changeIPRouting(currentFailoverIPServer):
            logger.info('Deleting IP routing for ' + failoverIP +
                        ' successful, setting new IP routing')

            # get first pingable server
            firstPingableServer = getFirstPingableServer()
            logger.info('Switching to: ' + firstPingableServer.shortName)

            # request change IP routing for current leader
            if (netcupAPI.changeIPRouting(firstPingableServer, netmask=failoverIPNetmask)):
                # set IP routing successful
                helper.sendNotification(body_setting_successful,
                                        pingableServer['id'].iloc[0])
                logger.info('setting up new IP routing for ' +
                            failoverIP + ' was successful')
                FIRST_PING_FAILED = False
            else:
                # set IP routing failed
                if not FAILOVER_ERROR_OCCURED == 'true':
                    # set new IP routing failed at first try
                    logger.error('setting new IP routing for ' + failoverIP +
                                 ' failed at first try, notification mail is sent')
                    sendNotification(body_setting_failed, return_set)
                    FAILOVER_ERROR_OCCURED = 'true'
                else:
                    # set new IP routing failed again
                    logger.error(
                        'another attempt for setting up new IP routing ' + failoverIP + ' failed')
        else:
            # delete IP routing failed
            if not FAILOVER_ERROR_OCCURED == 'true':
                # delete IP routing failed at first try
                FAILOVER_ERROR_OCCURED = 'true'
                logger.error('setting new IP routing for ' + failoverIP +
                             ' failed at first try, notification mail is sent')
                sendNotification(body_deleting_failed, return_del)
            else:
                # delete IP routing failed again
                logger.error(
                    'another attemmpt for deleting IP routing for ' + failoverIP + ' failed')
