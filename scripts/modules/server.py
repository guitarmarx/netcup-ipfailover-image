import pandas


class Server:
    id = ""
    name = ""
    mac = ""
    ip = ""

    def __init__(self.name):
        servers = pandas.read_csv(serverFile, sep=";", names=[
                                  "id", "name", "mac", "ip"])

    def getServerInfo(server_name):
        return servers[servers["name"] == server_name]
