FROM ubuntu:16.04


MAINTAINER meteorIT GbR Marcus Kastner

#Parameter Webservice
ENV SMTP_SERVER=localhost \
	SMTP_USER="<SMTP_USER>" \
	SMTP_PASS="<SMTP_PASS>" \
	SMTP_SOURCE_MAIL=failover@localhost \
	SMTP_TARGET_MAIL=target@localhost

#Parameter Webservice
ENV NETCUP_USER="<NETCUP_USER>" \
	NETCUP_PASS="<NETCUP_PASS>" \
	URL="https://www.vservercontrolpanel.de:443/WSEndUser?wsdl" \
	FAILOVER_IP="<FAILOVER_IP>" \
	FAILOVER_NETMASK="<FAILOVER_MASK>"
	
#Server Parameter
ENV TIME_BETWEEN_PINGS=60 \
    SERVER_1="<server_spitzname>;<server_name>;<mac>;<ip>"

WORKDIR /srv


RUN  apt-get update \
  && apt-get -y install gettext-base curl python python-pip iputils-ping \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
RUN pip install requests pandas 
COPY scripts/ /srv/scripts/
RUN chmod +x /srv/scripts/entrypoint.sh

ENTRYPOINT ["/srv/scripts/entrypoint.sh"]
