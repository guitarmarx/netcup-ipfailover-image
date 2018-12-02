import logging
import os
from modules.netcupapi import NetcupAPI
from modules import helper
from modules.slack import Slack
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
elif not (helper.checkIPFormat(os.environ['FAILOVER_IP'])):
    logger.error('Wrong format for parameter FAILOVER_IP...Abort')
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

    # failoverIP is reachable --> no action
    if netcupAPI.isFailoverIPPingable(timeBetweenPings):
        # wait 10 sec
        time.sleep(10)
        continue

    # failover ip is unreachable
    logger.warn('FailoverIP unreachable, check server ...')

    # get first pingable server
    firstPingableServer = netcupAPI.getFirstPingableServer(failoverServers)
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
        logger.info('FailoverIP assigned, continue monitoring...')
        time.sleep(10)
        continue
    else:
        logger.info('Current failover server is ' +
                    currentFailoverIPServer.nickname)

    if netcupAPI.isPingable(currentFailoverIPServer.ipAddress):
        # current assigned failoverIP server is reachable --> no action (netcup infrastcuture problem)
        logger.info(
            'Current failover server is reachable, failoverIP will not switched ...')
        continue

    if not netcupAPI.isNetcupAPIReachable():
        # current assigned failoverIP server is reachable --> no action (netcup infrastcuture problem)
        logger.info(
            'Netcup SCP API is unreachable, failoverIP cannot be swiched ... ')
        continue

    if isDryRun != 'FALSE':
        # dry run is active
        logger.info('Dry Run is active, no action ...')
        continue


#######    FAILOVER    #######
    # delete IP Routing
    logger.info("Delete FailoverIP from " +
                currentFailoverIPServer.nickname + " ... ")
    if netcupAPI.deleteFailoverIPRouting(currentFailoverIPServer):
        logger.info("FailoverIP routing deleted...")
        logger.info("Set new FailoverIP routing to " +
                    firstPingableServer.nickname + " ... ")
        if netcupAPI.setFailoverIPRouting(firstPingableServer):
            slack = Slack(slackWebhookURL, logger)
            slack.sendMessage(
                'Failover successfull from ' + currentFailoverIPServer.nickname + ' to ' + firstPingableServer.nickname)
        else:
            logger.error('Error in new Routing ... Restart')
            slack.sendMessage('Error in Failover ...')
    else:
        slack.sendMessage('Error in Failover ...')
