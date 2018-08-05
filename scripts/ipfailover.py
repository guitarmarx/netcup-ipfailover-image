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
smtpPassword = os.environ["SMTP_PASSWORD"]
smtpSourceMail = os.environ["SMTP_SOURCE_MAIL"]
smtpTargetMail = os.environ["SMTP_TARGET_MAIL"]

netcupUser = os.environ["NETCUP_USER"]
netcupPassword = os.environ["NETCUP_PASSWORD"]
netcupAPIUrl = os.environ["NETCUP_API_URL"]
failoverIP = os.environ["FAILOVER_IP"]
failoverIPNetmask = os.environ["FAILOVER_NETMASK"]

timeBetweenPings = os.environ["TIME_BETWEEN_PINGS"]
messages = helper.getMessages("messages.ini")
logFile = '/tmp/failover.log'
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
        logger.info('Starting failover...')

        currentFailoverIPServer = getCurrentIPFailoverServer()
        logger.info('Current failover server: ' + currentFailoverIPServer.name)

        # delete IP Routing
        if netcupAPI.deleteFailoverIPRouting(currentFailoverIPServer):
            logger.info('Deleting IP routing for ' + failoverIP +
                        ' successful, setting new IP routing')

            firstPingableServer = getFirstPingableServer()
            if netcupAPI.changeIPRouting(firstPingableServer, failoverIPNetmask):
                helper.sendNotification(
                    smtpServer, smtpPort, smtpUser, smtpPassword, smtpSourceMail, smtpTargetMail, "hello")
            else:
                logger.error("Error in new Routing")
        else:
            logger.error("Error in deleting IP Routing")
