FROM python:3.7.2-alpine

RUN pip install hbmqtt
RUN mkdir /hbmqtt
COPY configuration/config.yaml /hbmqtt
COPY configuration/password /hbmqtt
COPY configuration/server.crt configuration/server.key /hbmqtt/
COPY configuration/client.crt /hbmqtt
COPY runhbmqtt.sh /hbmqtt
RUN chmod 755 /hbmqtt/runhbmqtt.sh
CMD ["/hbmqtt/runhbmqtt.sh"]
