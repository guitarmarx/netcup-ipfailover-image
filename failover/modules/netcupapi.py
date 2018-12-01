import logging
from zeep import Client
from .vserver import VServer
import os
import time
import sys


class NetcupAPI:

    netcupAPIUrl = None
    netcupUser = None
    netcupPassword = None
    failoverIP = None
    failoverIPNetmask = None
    logger = None
    client = None

    def __init__(self, netcupAPIUrl, netcupUser, netcupPassword, failoverIP, failoverIPNetmask, logger):
        self.netcupAPIUrl = netcupAPIUrl
        self.netcupUser = netcupUser
        self.netcupPassword = netcupPassword
        self.failoverIP = failoverIP
        self.failoverIPNetmask = failoverIPNetmask
        self.logger = logger

        try:
            self.client = Client(self.netcupAPIUrl)
        except:
            logger.error("Netcup API " + netcupAPIUrl +
                         " is not reachable... Abort")
            sys.exit(1)

    def getAllVserverNames(self):
        vservers = self.client.service.getVServers(
            loginName=self.netcupUser, password=self.netcupPassword)
        return vservers

    def getVserverState(self, vServerName):
        state = self.client.service.getVServerState(
            loginName=self.netcupUser, password=self.netcupPassword, vserverName=vServerName)
        return state

    def getVServerLoad(self, vServerName):
        load = self.client.service.getVServerLoad(
            loginName=self.netcupUser, password=self.netcupPassword, vserverName=vServerName)
        return load

    def getVServerUptime(self, vServerName):
        uptime = self.client.service.getVServerUptime(
            loginName=self.netcupUser, password=self.netcupPassword, vserverName=vServerName)
        return uptime

    def getVServerProcesses(self, vServerName):
        processes = self.client.service.getVServerProcesses(
            loginName=self.netcupUser, password=self.netcupPassword, vserverName=vServerName)
        return processes

    def getAllIPsFromVServer(self, vServerName):
        ipadresses = self.client.service.getVServerIPs(
            loginName=self.netcupUser, password=self.netcupPassword, vserverName=vServerName)
        return ipadresses

    def getVServerIP(self, vServerName, failoverIP):
        ipadresses = self.getAllIPsFromVServer(vServerName)
        for ip in ipadresses:
            if failoverIP not in ip:
                return ip

    def hasVServerFailoverIP(self, vServerName):
        ipadresses = self.getAllIPsFromVServer(vServerName)
        if self.failoverIP in ipadresses:
            return True
        else:
            return False

    def getVServerMac(self, vServerName):
        mac = self.client.service.getVServerMac(
            loginName=self.netcupUser, password=self.netcupPassword, vserverName=vServerName)
        return mac

    def setFailoverIPRouting(self, vServer):
        try:
            message = self.client.service.changeIPRouting(
                loginName=self.netcupUser, password=self.netcupPassword, destinationvserverName=vServer.netcupServerName, routedIP=self.failoverIP, routedMask=self.failoverIPNetmask, destinationInterfaceMAC=vServer.macAddress)
            self.logger.debug(message)
            return True
        except:
            return False

    def deleteFailoverIPRouting(self, vServer):
        try:
            message = self.client.service.changeIPRouting(
                loginName=self.netcupUser, password=self.netcupPassword, destinationvserverName=vServer.netcupServerName, routedIP=self.failoverIP, routedMask=self.failoverIPNetmask, destinationInterfaceMAC='00:00:00:00:00:00')
            self.logger.debug(message)
            return True
        except:
            return False

    def getVServerInformation(self, vServerName):
        info = self.client.service.getVServerInformation(
            loginName=self.netcupUser, password=self.netcupPassword, vservername=vServerName)
        return info

    def getVServerNickname(self, vServerName):
        nickname = self.client.service.getVServerNickname(
            loginName=self.netcupUser, password=self.netcupPassword, vservername=vServerName)
        return nickname

    """ def getVservers(self):
        for vServerName in self.getAllVserverNames():
            nickname = self.getVServerNickname(vServerName)
            ipAddress = self.getVServerIPs(vServerName)
            print(vServerName)
            print(nickname)
            print(ipAddress)
    """

    def createFailoverServerObject(self, vServerName, vServerMac):
        vServerName = vServerName
        vServerMac = vServerMac
        vServerNickname = self.getVServerNickname(vServerName)
        vServerIP = self.getVServerIP(vServerName, self.failoverIP)

        vServer = VServer(vServerName, vServerNickname,
                          vServerMac, vServerIP)
        return vServer

    def getAllFailoverServers(self):
        # get parameter from ENVIRONMENT

        failoverServers = []
        failoverServerNames = []
        failoverServerMacs = []

        for env in os.environ:
            if "FAILOVER_SERVER_MAC" in env:
                failoverServerMacs.append(os.environ[env])
            elif "FAILOVER_SERVER_" in env:
                failoverServerNames.append(os.environ[env])

        for i in range(len(failoverServerNames)):
            vServer = self.createFailoverServerObject(
                failoverServerNames[i], failoverServerMacs[i])
            failoverServers.append(vServer)

        return failoverServers

    def getCurrentIPFailoverServer(self, failoverServers):
        for failoverServer in failoverServers:
            # check if server has failover ip
            if self.hasVServerFailoverIP(failoverServer.netcupServerName):
                return failoverServer
        return None

    def isFailoverIPPingable(self, timeBetweenPings):
        isFailoverIPPingable = True

        if not self.isPingable(self.failoverIP):
            # start wait time
            self.logger.warn("First ping to failoverIP failed, wait " +
                             str(timeBetweenPings) + " seconds ...")
            time.sleep(timeBetweenPings)

            # Second Try: ping failover IP
            if not self.isPingable(self.failoverIP):
                isFailoverIPPingable = False
                self.logger.warn("Second ping to failoverIP failed ...")
            else:
                self.logger.info("FailoverIP back to normal ...")
        return isFailoverIPPingable

    def isPingable(self, ip):
        command = "ping -c 1 -W 4 " + ip + " > /dev/null 2>&1"
        response = os.system(command)

        if response == 0:
            return True
        else:
            return False

    def isNetcupAPIReachable(self):
        try:
            self.getAllVserverNames()
            return True
        except:
            self.logger.error('Netcup api is not reachable...Abort!')
            return False
