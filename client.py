import logging
import asyncio
import os
import argparse

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


def mk_argparse():
    ap = argparse.ArgumentParser()
    ap.add_argument('mqtturl', 
                    help='URL to the mqtt server, for example '
                    'mqtts://iot:password@localhost:8883/')
    ap.add_argument('cafile', help='cafile to use for ssl verification.  This '
                    'should be the server\'s certificate file.')
    return ap


@asyncio.coroutine
def uptime_coro(url, cafile):
    C = MQTTClient()
    yield from C.connect(url, cafile=cafile)

    # Subscribe to '$SYS/broker/uptime' with QOS=1
    # Subscribe to '$SYS/broker/load/#' with QOS=2
    yield from C.subscribe([
            ('$SYS/broker/uptime', QOS_1),
            ('$SYS/broker/load/#', QOS_2),
         ])
    try:
        for i in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print("%d:  %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        yield from C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


def main():
    opts = mk_argparse().parse_args()

    if not os.path.exists(opts.cafile):
        return f'{opts.cafile} does not exist.'

    asyncio.get_event_loop().run_until_complete(uptime_coro(opts.mqtturl, 
                                                            opts.cafile))


if __name__ == '__main__':
    main()