FROM docker.io/alpine:latest

RUN apk --no-cache add python3 wget curl net-tools telnet && \
    python3 -m venv /opt/panda && \
    /opt/panda/bin/pip install -U pip && \
    /opt/panda/bin/pip install -U setuptools && \
    /opt/panda/bin/pip install -U stomp.py

RUN mkdir -p /data/panda && \
    chmod 777 /data/panda

CMD exec /bin/sh -c "trap : TERM INT; sleep infinity & wait"

EXPOSE 25080 25443
