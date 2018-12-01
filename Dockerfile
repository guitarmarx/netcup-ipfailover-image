FROM python:3.6-slim

LABEL maintainer="meteorIT GbR Marcus Kastner"

ENV NETCUP_API_URL = "https://www.vservercontrolpanel.de:443/WSEndUser?wsdl" \
	NETCUP_USER="" \
	NETCUP_PASSWORD="" \
	FAILOVER_IP="" \
	FAILOVER_NETMASK=32 \
	TIME_BETWEEN_PINGS=60 \
	FAILOVER_SERVER_1="" \
	FAILOVER_SERVER_MAC_1=""\
	SLACK_WEBHOOK_URL=https://hooks.slack.com/services/<TOKEN> \
	DRY_RUN=FALSE

RUN apt update \
	&& apt install -y iputils-ping \
	&& pip install --no-cache-dir zeep

COPY failover/ /srv/failover/

ENTRYPOINT ["python","/srv/failover/failover.py"]
