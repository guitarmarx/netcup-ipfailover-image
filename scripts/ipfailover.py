import logging
import os
from modules.netcupapi import NetcupAPI
from modules import helper
from modules.server import Server
from modules.mailsender import Mailsender


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

logLevelArray = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}
logLevel = logLevelArray[os.environ["LOG_LEVEL"]]

# Init Logger
logger = helper.initLogging(logFormat, logLevel, logFile)
logger.info("FailoverIP monitoring is active ...")

# read failover server
failoverServers = helper.getFailoverServers()
logger.info("Configured failover servers: " + failoverServers)

# create netcupAPI object
netcupAPI = NetcupAPI(netcupAPIUrl, netcupUser, netcupPassword,
                      failoverIP, failoverIPNetmask, logger)


def getCurrentIPFailoverServer():
    for failoverServer in failoverServers:
        # check if server has failover ip
        if netcupAPI.hasServerFailoverIP(failoverServer):
            return failoverServer


def getFirstPingableServer():
    for failoverServer in failoverServers:
        if failoverServer.isPingable():
            return failoverServer


while True:
    if not helper.isFailoverIPPingable(failoverIP, timeBetweenPings):
        logger.info('FailoverIP unreachable, start failover ...')

        currentFailoverIPServer = getCurrentIPFailoverServer()

        # delete IP Routing
        logger.info("delete FailoverIP from " +
                    currentFailoverIPServer.shortName + " ... ")
        if netcupAPI.deleteFailoverIPRouting(currentFailoverIPServer):
            logger.info("FailoverIP deleted!")

            firstPingableServer = getFirstPingableServer()
            logger.info("route new FailoverIP to  " +
                        currentFailoverIPServer.shortName + " ... ")
            if netcupAPI.setFailoverIP(firstPingableServer):
                Mailsender.sendNotification('subject', 'body')

            else:
                logger.error("Error in new Routing")
        else:
            logger.error("Error in deleting IP Routing")
