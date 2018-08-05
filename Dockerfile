FROM python:3-alpine3.7

LABEL maintainer="meteorIT GbR Marcus Kastner"

ENV SMTP_SERVER=localhost \
	SMTP_PORT=25 \
	SMTP_USER="<SMTP_USER>" \
	SMTP_PASSWORD="<SMTP_PASS>" \
	SMTP_SOURCE_MAIL=failover@localhost \
	SMTP_TARGET_MAIL=target@localhost \
	NETCUP_USER="<NETCUP_USER>" \
	NETCUP_PASSWORD="<NETCUP_PASSWORD>" \
	NETCUP_API_URL="https://www.vservercontrolpanel.de:443/WSEndUser?wsdl" \
	FAILOVER_IP="<FAILOVER_IP>" \
	FAILOVER_NETMASK="<FAILOVER_MASK>" \
	TIME_BETWEEN_PINGS=60 \
	SERVER_1="<server_spitzname>;<server_name>;<mac>;<ip>"

RUN apk update && \
	apk add iputils \
	&& pip install --no-cache-dir requests ConfigParser


COPY scripts/ /tmp/scripts/
RUN chmod +x /tmp/scripts/entrypoint.sh

ENTRYPOINT ["/tmp/scripts/entrypoint.sh"]
