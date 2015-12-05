#!/bin/bash

docker run \
    --name=dnsbin \
    --rm=true \
    --net=host \
    -e DNS_ZONE=paste \
    -e DNS_KEY_ALGO=hmac-sha512 \
    -e DNS_KEY_NAME=paste \
    -e DNS_KEY_SECRET="974Dq4TkBfv50g7zLvBH+5Fx+Sngl27IPxIb5tuLjErm34nWyW07ACKqdYTafvAXFkHI3HzRFOV5Zz18Zuvw1w==" \
    -it dnsbin
