# Libraries
import smtplib
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText
import logging
import subprocess
import os
import pandas
import requests
import re
import time
from modules.netcupapi import NetcupAPI
from modules import helper


#####     PARAMETER     #####
# netcupUser = os.environ["NETCUP_USER"]
# netcupPass = os.environ["NETCUP_PASS"]
# netcupAPIUrl = os.environ["NETCUP_API_URL"]
# failoverIP = os.environ["FAILOVER_IP"]
# failoverIPNetmask = os.environ["FAILOVER_NETMASK"]

# smtpServer = os.environ["SMTP_SERVER"]
# smtpPort = os.environ["SMTP_PORT"]
# smtpUser = os.environ["SMTP_USER"]
# smtpPass = os.environ["SMTP_PASS"]
# smtpSourceMail = os.environ["SMTP_SOURCE_MAIL"]
# smtpTargetMail = os.environ["SMTP_TARGET_MAIL"]

# timeBetweenPings = os.environ["TIME_BETWEEN_PINGS"]
serverFile = "..conf/servers.conf"
failoverErrorOccured = False
# messages = helper.getMessages("messages.ini")

#### get servers     ####
servers = pandas.read_csv(serverFile, sep=";", names=[
                          "id", "name", "mac", "ip"])

for server in servers:
    print(server)


# def getCurrentIPFailoverServer():
#     # reading available leaders
#     servers = pandas.read_csv(serverFile, sep=";", names=[
#         "id", "name", "mac", "ip"])
#     for element in servers["name"]:
#         # check if server has failover ip
#         if helper.hasServerFailoverIP(element):
#             return servers[servers["name"] == element]
#     return False


# def getFirstPingableServer():
#     servers = pandas.read_csv(serverFile, sep=";", names=[
#         "id", "name", "mac", "ip"])
#     for element in servers["ip"]:
#         # check if server is pingable
#         if helper.isPingable(element):
#             return servers[servers["ip"] == element]
#     return False


# # ----------------MAIN----------------------------


# # Init Logger
# logger = helper.initLogging()
# logger.info("script started ...")

# FIRST_PING_FAILED = False


# while True:
#     time.sleep(TIME_BETWEEN_PINGS)

#     # check ping
#     if isPingable(failoverIP):
#         FIRST_PING_FAILED = False
#         continue
#     # ping = False
#     if FIRST_PING_FAILED == False:
#         logger.warn('First attempt: Ping lost to ' + failoverIP +
#                     '. Setting FIRST_PING_FAILED Flag.')
#         FIRST_PING_FAILED = True
#         continue

#     # ping = False && FIRST_PING_FAILED = True
#     logger.error('Second attempt: Ping lost to ' + failoverIP)
#     logger.info('Starting failover...')

#     # Start Failover
#     # get server with failoverIP
#     failoverIPServer = getCurrentIPFailoverServer()
#     logger.info('Current failover server: ' + failoverIPServer['id'].iloc[0])

#     # delete IP Routing
#     return_del = changeIPRouting(
#         netcup_user, netcup_pass, failoverIPServer['name'].iloc[0], failoverIP, failoverIPNetmask, '00:00:00:00:00:00')

#     if return_del == 'true':
#         # delete IP routing successful
#         logger.info('Deleting IP routing for ' + failoverIP +
#                     ' successful, setting new IP routing')

#         # get first pingable server
#         pingableServer = getFirstPingableServer()
#         logger.info('Switching to: ' + pingableServer['id'].iloc[0])

#         # request change IP routing for current leader
#         return_set = changeIPRouting(
#             netcup_user, netcup_pass, pingableServer['name'].iloc[0], failoverIP, failoverIPNetmask, pingableServer['mac'].iloc[0])

#         if return_set == 'true':
#             # set IP routing successful
#             sendNotification(body_setting_successful,
#                              pingableServer['id'].iloc[0])
#             logger.info('setting up new IP routing for ' +
#                         failoverIP + ' was successful')
#             FIRST_PING_FAILED = False
#         else:
#             # set IP routing failed
#             if not FAILOVER_ERROR_OCCURED == 'true':
#                 # set new IP routing failed at first try
#                 logger.error('setting new IP routing for ' + failoverIP +
#                              ' failed at first try, notification mail is sent')
#                 sendNotification(body_setting_failed, return_set)
#                 FAILOVER_ERROR_OCCURED = 'true'
#             else:
#                 # set new IP routing failed again
#                 logger.error(
#                     'another attempt for setting up new IP routing ' + failoverIP + ' failed')
#     else:
#         # delete IP routing failed
#         if not FAILOVER_ERROR_OCCURED == 'true':
#             # delete IP routing failed at first try
#             FAILOVER_ERROR_OCCURED = 'true'
#             logger.error('setting new IP routing for ' + failoverIP +
#                          ' failed at first try, notification mail is sent')
#             sendNotification(body_deleting_failed, return_del)
#         else:
#             # delete IP routing failed again
#             logger.error(
#                 'another attemmpt for deleting IP routing for ' + failoverIP + ' failed')
