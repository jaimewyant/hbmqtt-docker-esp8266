HBMQTT-ESP8266-MICROPYTHON
==========================

This repository provides a pre-configured MQTT broker along with a sample
micropython / CPython MQTT client.  

Build the docker image:

```bash
$ docker build -t hbmqtt:1.0 .
```

Run the docker image.  This binds to 127.0.0.1.  You will *not* be able to
connect from any computer but the one **running** the MQTT broker.  If you
want to open the server up, remove the 127.0.0.1:.

    docker run --rm -it --name mqtt -p 127.0.0.1:8883:8883 hbmqtt:1.0

Connect to the broker with the sample client using this command line:

```
$ python client.py mqtts://iot:password@localhost:8883/ configuration/server.crt
```

Odds are the above command will not work.  You need to setup a virtualenv with 
hbmqtt installed.  If you have [poetry](https://poetry.eustace.io/) then run

```bash
$ poetry install
```

To run the client inside of poetry::

```bash
$ poetry run python client.py mqtts://iot:password@localhost:8883/ configuration/server.crt 
```

Configuration
-------------
Don't run the MQTT server with the default settings (the keys are here in 
github!).  Instead, configure the docker with your own settings.  First,
generate new keys using the support/mkcert.sh script.

```bash
# Specify localhost for local testing.
$ ./support/mkcert.sh localhost
Generating a RSA private key
.....+++++
........................................................+++++
writing new private key to 'server.key'
-----
Generating a RSA private key
.........+++++
.......+++++
writing new private key to 'client.key'
-----
Moving certificate files to the configuration directory.
renamed 'server.key' -> 'configuration/server.key'
renamed 'server.crt' -> 'configuration/server.crt'
renamed 'client.key' -> 'configuration/client.key'
renamed 'client.crt' -> 'configuration/client.crt'
```

Next, setup new users.  First, delete the current password file, then use 
support/createuser.sh to create new users.  createuser.sh takes two arguments 
the username and password.  (You may need to install mkpasswd - for me it was
apt-get install whois)

```bash
$ rm configuration/password
# username password are the arguments.
$ ./support/createuser.sh iot password
```

Finally, remake the image with your changes:

```bash
$ docker build -t hbmqtt:1.0 .
```

ESP2866
-------
This configuration / code was tested with [esp8266 firmware V1.10](https://micropython.org/resources/firmware/esp8266-20190125-v1.10.bin).  If you want to try the mqtt client on your 8266, then edit the esp8266/mqttclient.py script, changing the constants declared at the top.

Four files need to be copied to the esp8266 board.  First, copy your client
certificates.  These will be in the esp8266 directory.  They are created when
the mkcert.sh script is run.  Below is how I copy the files using rshell.

```bash
$ poetry run rshell -p com10 cp client.crt.der client.key.der /pyboard/
```

Next, copy the mqttclient.py script you edited, along with the umqttsimple.py
script.

```bash
$ poetry run rshell -p com10 cp esp8266/*.py /pyboard
```

Finally execute the 