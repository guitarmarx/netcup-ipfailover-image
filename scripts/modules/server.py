import os


class Server:
    # Example: "meteor03-prod;v22017083665152308;a6:2a:17:93:9e:d3;188.68.38.72"
    netcupServerName = ""
    shortName = ""
    mac = ""
    ip = ""

    def __init__(self, netcupServerName, shortName, mac, ip):
        self.netcupServerName = netcupServerName
        self.shortName = shortName
        self.mac = mac
        self.ip = ip

    def isPingable(self):
        command = "ping -c 1 -W 4 " + self.ip + " > /dev/null 2>&1"
        response = os.system(command)

        if response == 0:
            return True
        else:
            return False

    def printInfo(self):
        print("ID: " + self.netcupServerName + " NAME: " + self.shortName +
              " MAC: " + self.mac + " IP: " + self.ip)
