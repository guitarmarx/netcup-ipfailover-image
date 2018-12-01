import os
import logging
import time
import requests
import socket


def getFirstPingableServer(failoverServers):
    for failoverServer in failoverServers:
        if failoverServer.isPingable():
            return failoverServer


def initLogging(logFormat, logLevel,  logFile):
    logger = logging.getLogger()
    logger.setLevel(logLevel)
    formatter = logging.Formatter(logFormat)

    # Init file logging
    handler = logging.FileHandler(logFile)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Init console logging
    handler2 = logging.StreamHandler()
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
    return logger


def checkParameterAvailable():
    parameterList = ['NETCUP_USER', 'NETCUP_PASSWORD',
                     'FAILOVER_IP', 'FAILOVER_SERVER_MAC_1', 'FAILOVER_SERVER_1', 'NETCUP_API_URL', 'FAILOVER_NETMASK', 'SLACK_WEBHOOK_URL', 'TIME_BETWEEN_PINGS']
    for parameter in parameterList:
        try:
            os.environ[parameter]
        except KeyError:
            print("Missing parameter " + parameter + "...Abort!")
            return False
    return True


def checkFailoverIP(ipAddress):
    try:
        socket.inet_aton(ipAddress)
        return True
    except socket.error:
        return False


def checkNetcupUserLogin():
    if os.environ['NETCUP_USER'] is not None and os.environ['NETCUP_PASSWORD']:
        return True
    else:
        return False


def checkFailoverServers():
    # Server Parmeter abrufen
    failoverServer = []
    failoverServerMac = []

    for env in os.environ:
        if "FAILOVER_SERVER_MAC" in env:
            failoverServerMac.append(env)
        elif "FAILOVER_SERVER_" in env:
            failoverServer.append(env)

    if len(failoverServer) is not len(failoverServerMac):
        return False
    else:
        return True
