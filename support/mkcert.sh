#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Specify the hostname"
    exit 1
fi

# Generate the server key - it is 1024 bits.  When trying larger keys, the ESP8266 had
# trouble connecting.  However, the client key *has* to be larger (2048) or things don't
# work.  I'm no SSL wizard, once I made it work, I did a back flip and proceded to forget
# the experience.
openssl req -new -newkey rsa:1024 -days 3650 -nodes -x509 -keyout server.key -out server.crt \
     -subj "/C=US/ST=MS/L=BT/O=hbmqtt/OU=hbmqtti node/CN=$1"

# Generate the client key (2048 bits, dont change that.)
openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 -keyout client.key -out client.crt \
     -subj "/C=US/ST=MS/L=BT/O=hbmqtt/OU=hbmqtti node/CN=CLIENT"

# Create DER formatted cert/key.
openssl x509 -in client.crt -out esp8266/client.crt.der -outform DER
openssl rsa -in client.key -out esp8266/client.key.der -outform DER

echo 'Moving certificate files to the configuration directory.'
mv -v server.key server.crt client.key client.crt configuration/
