import logging
import os
from modules.netcupapi import NetcupAPI
from modules import helper
from modules.vserver import VServer
import sys

# check parameter
###################################
if not helper.checkParameterAvailable():
    sys.exit(1)
elif not (helper.checkFailoverIP(os.environ['FAILOVER_IP'])):
    print('Missing parameter FAILOVER_IP...Abort')
    sys.exit(1)
elif not helper.checkNetcupUserLogin():
    print('Missing parameter NETCUP_USER or NETCUP_PASSWORD...Abort')
    sys.exit(1)
elif not helper.checkFailoverServers():
    print('incorrect parameter count for FAILOVER_SERVER_MAC_X and FAILOVER_SERVER_X...Abort')
    sys.exit(1)
else:
    sys.exit(0)


#####     PARAMETER     #####
netcupAPIUrl = os.environ["NETCUP_API_URL"]
netcupUser = os.environ["NETCUP_USER"]
netcupPassword = os.environ["NETCUP_PASSWORD"]
failoverIP = os.environ["FAILOVER_IP"]
failoverIPNetmask = os.environ["FAILOVER_NETMASK"]
isDryRun = os.environ["DRY_RUN"]

slackWebhookURL = os.environ['SLACK_WEBHOOK_URL']

timeBetweenPings = os.environ["TIME_BETWEEN_PINGS"]
logFile = '/var/log/failover.log'
logFormat = '%(asctime)s - %(levelname)s - %(message)s'
logLevel = 'INFO'

# Init Logger
logger = helper.initLogging(logFormat, logLevel, logFile)
logger.info("FailoverIP monitoring is active ...")

# create netcupAPI object
netcupAPI = NetcupAPI(netcupAPIUrl, netcupUser, netcupPassword,
                      failoverIP, failoverIPNetmask, logger)

# read failover server
failoverServers = netcupAPI.getAllFailoverServers()


while True:
    if not netcupAPI.isFailoverIPPingable(timeBetweenPings):

        # failover ip is unreachable
        logger.info('FailoverIP unreachable, check server ...')

        # get current failover server
        currentFailoverIPServer = netcupAPI.getCurrentIPFailoverServer(
            failoverServers)

        # ping current failover server
        if not netcupAPI.isPingable(currentFailoverIPServer.ipAddress) or netcupAPI.isNetcupAPIReachable():

            if 'FALSE' not in isDryRun:
                # server is unreachable --> Start Failover
                # delete IP Routing
                logger.info("delete FailoverIP from " +
                            currentFailoverIPServer.nickname + " ... ")
                if netcupAPI.deleteFailoverIPRouting(currentFailoverIPServer):
                    logger.info("FailoverIP deleted!")

                    firstPingableServer = helper.getFirstPingableServer(
                        failoverServers)
                    logger.info("route new FailoverIP to  " +
                                currentFailoverIPServer.shortName + " ... ")
                    if netcupAPI.setFailoverIPRouting(firstPingableServer):
                        helper.sendSlackMessage(
                            slackWebhookURL, 'Failover successfull')

                    else:
                        logger.error("Error in new Routing")
                else:
                    logger.error("Error in deleting IP Routing")
            else:
                logger.error(
                    "dry run is active ... failover won't be executed ...")
        else:
            logger.error("netcup problem, no action")
