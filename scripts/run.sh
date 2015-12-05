#!/bin/sh

if ! [ -f /var/cache/bind/db.$DNS_ZONE ]; then
    j2 -f env /templates/db.blank_zone.j2 > /var/cache/bind/db.$DNS_ZONE
    chown named:named /var/cache/bind/db.$DNS_ZONE
fi;

j2 -f env /templates/named.conf.local.j2 > /etc/bind/named.conf.local
j2 -f env /templates/nsupdate.key.j2 > /etc/bind/nsupdate.key
j2 -f env /templates/dnsbin.ini.j2 > /etc/dnsbin.ini

gunicorn \
    -b :80 \
    -w 32 \
    --chdir /usr/app \
    --access-logfile /dev/stdout \
    --error-logfile /dev/stdout \
    api:app &
/usr/sbin/named -u named -g -4
