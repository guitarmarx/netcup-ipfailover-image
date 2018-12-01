import logging
import os
from modules.netcupapi import NetcupAPI
from modules import helper
from modules.vserver import VServer
import sys
import time

# init logging
logFile = '/var/log/failover.log'
logFormat = '%(asctime)s - %(levelname)s - %(message)s'
logLevel = os.environ["LOG_LEVEL"]

# Init Logger
logger = helper.initLogging(logFormat, logLevel, logFile)


# check parameter
###################################
if not helper.checkParameterAvailable():
    sys.exit(1)
elif not (helper.checkFailoverIP(os.environ['FAILOVER_IP'])):
    logger.error('Missing parameter FAILOVER_IP...Abort')
    sys.exit(1)
elif not helper.checkNetcupUserLogin():
    logger.error('Missing parameter NETCUP_USER or NETCUP_PASSWORD...Abort')
    sys.exit(1)
elif not helper.checkFailoverServers():
    logger.error(
        'incorrect parameter count for FAILOVER_SERVER_MAC_X and FAILOVER_SERVER_X...Abort')
    sys.exit(1)


#####     PARAMETER     #####
netcupAPIUrl = os.environ["NETCUP_API_URL"]
netcupUser = os.environ["NETCUP_USER"]
netcupPassword = os.environ["NETCUP_PASSWORD"]
failoverIP = os.environ["FAILOVER_IP"]
failoverIPNetmask = os.environ["FAILOVER_NETMASK"]
isDryRun = os.environ["DRY_RUN"]
logger.debug(isDryRun)

slackWebhookURL = os.environ['SLACK_WEBHOOK_URL']

timeBetweenPings = int(os.environ["TIME_BETWEEN_PINGS"])

# create netcupAPI object
netcupAPI = NetcupAPI(netcupAPIUrl, netcupUser, netcupPassword,
                      failoverIP, failoverIPNetmask, logger)

# read failover server
failoverServers = netcupAPI.getAllFailoverServers()

logger.info("FailoverIP monitoring is active ...")
while True:
    if not netcupAPI.isFailoverIPPingable(timeBetweenPings):

        # failover ip is unreachable
        logger.warn('FailoverIP unreachable, check server ...')

        # get first pingable server
        firstPingableServer = helper.getFirstPingableServer(failoverServers)
        logger.info('First reachable server is ' +
                    firstPingableServer.nickname)

        # get current failover server
        currentFailoverIPServer = netcupAPI.getCurrentIPFailoverServer(
            failoverServers)

        if currentFailoverIPServer is None:
            #FailoverIP is not assigned
            logger.warn('FailoverIP is not assigned. Assign to ' +
                        firstPingableServer.nickname)
            netcupAPI.setFailoverIPRouting(firstPingableServer)
            logger.info('FailoverIP assigned, restart monitoring...')
            continue
        else:
            logger.info('current failover server is ' +
                        currentFailoverIPServer.nickname)

            # ping current failover server
        if not netcupAPI.isPingable(currentFailoverIPServer.ipAddress) or netcupAPI.isNetcupAPIReachable():

            if isDryRun == 'FALSE':
                # server is unreachable --> Start Failover
                # delete IP Routing
                logger.info("delete FailoverIP from " +
                            currentFailoverIPServer.nickname + " ... ")
                if netcupAPI.deleteFailoverIPRouting(currentFailoverIPServer):
                    logger.info("FailoverIP deleted!")

                    logger.info("route new FailoverIP to  " +
                                currentFailoverIPServer.nickname + " ... ")
                    if netcupAPI.setFailoverIPRouting(firstPingableServer):
                        helper.sendSlackMessage(
                            slackWebhookURL, 'Failover successfull from ' + currentFailoverIPServer.nickname + ' to ' + firstPingableServer)

                    else:
                        logger.error("Error in new Routing ... Restart ...")
                else:
                    logger.error("Error in deleting IP Routing ... Restart.")
            else:
                logger.info(
                    "dry run is active ... failover won't be executed ...")
        else:
            logger.error("netcup problem, no action")
    # wait 10 sec
    time.sleep(10)
