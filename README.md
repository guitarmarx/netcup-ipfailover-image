# Netcup IPFailover Image

This docker image deploys uses netcup scp api to reassign a netcup failoverIP, if a server fails.

#### Requirements

To use this image you need netcup as your server infrastructure provider. You also have to purchase and enable the netcup failoverIP service. More information can be found here: https://www.netcup.de/bestellen/produkt.php?produkt=1073

## Quickstart

#### Build Image
```sh
docker build -t <image_name>:<image_version> .
```
#### Run Container
```sh
docker run -d \
        -e NETCUP_USER=<NETCUP_USER> \
        -e NETCUP_PASSWORD=<NETCUP_PASSWORD> \
        -e FAILOVER_IP=<FAILOVER_IP> \
        -e FAILOVER_SERVER_1=<FAILOVER_SERVER_1> \
        -e FAILOVER_SERVER_MAC_1=<FAILOVER_SERVER_MAC_1> \
        <image>:<version>
```

# Configuration
#### Optional Parameters:

You can add multiple netcup server for the failover with the parameters FAILOVER_SERVER_1 and  FAILOVER_SERVER_MAC_1. Just increment the last number.

Parameter | Function| Default Value|
---|---|---|
NETCUP_API_URL |Netcup SCP Webservice API | https://www.vservercontrolpanel.de:443/WSEndUser?wsdlv
NETCUP_USER | Netcup user  | -
NETCUP_PASSWORD | Netcup Password | -
FAILOVER_SERVER_LIST | Netcup comma separated server list name e.g. "v22016063665435548,v22016063665435512"| -
SLACK_WEBHOOK_URL | Slack webhook url | https://hooks.slack.com/services/<TOKEN>
TIME_BETWEEN_PINGS | Time between two pings in seconds, after that, a failover will be initiated | 60
DRY_RUN | if set, the container monitors the failover ip, but won't reassign the failoverIP if a server is down | FALSE
LOG_LEVEL | Log level. To view the log you can navigate to the log file /var/log/failover.log | INFO
FAILOVER_IP | Netcup failover IP | -





