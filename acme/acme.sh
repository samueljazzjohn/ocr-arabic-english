#!/bin/sh

FILE=/etc/traefik/acme/acme.json

if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    touch $FILE
    chmod 600 $FILE
fi
