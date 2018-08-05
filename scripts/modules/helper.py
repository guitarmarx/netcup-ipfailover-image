import os
import logging
import time

from .server import Server
import configparser


def getFailoverServers():

    # read failover server strings
    serversStrings = []
    failoverServers = []
    for parameter in os.environ:
        if "SERVER_" in parameter:
            serversStrings.append((os.environ[parameter]))

    # split strings and create server objects
    for serverString in serversStrings:
        serverInfos = serverString.split(';')
        failoverServer = Server(
            serverInfos[0], serverInfos[1], serverInfos[2], serverInfos[3])
        failoverServers.append(failoverServer)

    return failoverServers


def isFailoverIPPingable(failoverIP, timeBetweenPings):
    isFailoverIPPingable = True

    if not isPingable(failoverIP):
        # start wait time
        time.sleep(timeBetweenPings)

        # Second Try: ping failover IP
        if not isPingable(failoverIP):
            isFailoverIPPingable = False

    return isFailoverIPPingable


def getMessages(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config


def isPingable(ip):
    command = "ping -c 1 -W 4 " + ip + " > /dev/null 2>&1"
    response = os.system(command)

    if response == 0:
        return True
    else:
        return False


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
