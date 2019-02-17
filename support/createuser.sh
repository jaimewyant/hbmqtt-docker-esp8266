#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Specify username password"
    exit 1
fi

passwd=$(mkpasswd -m sha-512 $2)

echo "$1:$passwd" >> configuration/password
