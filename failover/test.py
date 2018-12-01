import socket
from modules.netcupapi import NetcupAPI
from modules.vserver import VServer
from modules import helper

# init logging
logFile = 'failover.log'
logFormat = '%(asctime)s - %(levelname)s - %(message)s'
logLevel = 'DEBUG'

# Init Logger
logger = helper.initLogging(logFormat, logLevel, logFile)

netcupAPI = NetcupAPI('https://www.vservercontrolpanel.de:443/WSEndUser?wsdl', '48701', 'NMtvqJP7c/+R',
                      '188.68.44.180', '32', logger)


vServerName = 'v22018063665168274'
vServerMac = 'da:88:7b:d4:35:5f'
vServerNickname = netcupAPI.getVServerNickname(vServerName)
vServerIP = netcupAPI.getVServerIP(vServerName, '188.68.44.180')

vServer = VServer(vServerName, vServerNickname,
                  vServerMac, vServerIP)

netcupAPI.setFailoverIPRouting(vServer)
