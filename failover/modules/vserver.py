import os


class VServer:
    netcupServerName = ""
    nickname = ""
    macAddress = ""
    ipAddress = ""

    def __init__(self, netcupServerName, nickname, macAddress, ipAddress):
        self.netcupServerName = netcupServerName
        self.nickname = nickname
        self.macAddress = macAddress
        self.ipAddress = ipAddress

    def isPingable(self):
        command = "ping -c 1 -W 4 " + self.ipAddress + " > /dev/null 2>&1"
        response = os.system(command)

        if response == 0:
            return True
        else:
            return False
