from modules.netcupapi import NetcupAPI

netcupAPIUrl = 'https://www.servercontrolpanel.de:443/WSEndUser?wsdl'
netcupUser = '48701'
netcupPassword = 'NMtvqJP7c/+R'
failoverIP = '188.68.44.180'
failoverIPNetmask = '32'
logger = None

netcupAPI = NetcupAPI(netcupAPIUrl, netcupUser, netcupPassword,
                      failoverIP, failoverIPNetmask, logger)


server = netcupAPI.getAllVserverNames()

for s in server:
    print(netcupAPI.getAllIPsFromVServer(s))


test = "v1,v2,v3"

sep = test.split(',')
print(sep)
