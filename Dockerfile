FROM python:3-alpine3.7

LABEL maintainer="meteorIT GbR Marcus Kastner"

ENV NETCUP_API_URL = 'https://www.vservercontrolpanel.de:443/WSEndUser?wsdl' \
	NETCUP_USER="" \
	NETCUP_PASSWORD="" \
	FAILOVER_IP="" \
	FAILOVER_NETMASK=32 \
	TIME_BETWEEN_PINGS=60 \
	FAILOVER_SERVER_1="" \
	FAILOVER_SERVER_MAC_1=""\
	SLACK_WEBHOOK_URL=https://hooks.slack.com/services/<TOKEN> \
	DRY_RUN=FALSE

RUN apk update \
	&& apk add iputils \
	&& pip install --no-cache-dir zeep

COPY scripts/ /srv/scripts/

ENTRYPOINT ["python","/srv/scripts/failover.py"]
