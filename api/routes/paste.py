#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                Version 2, December 2004

 Copyright (C) 2015 Thomas Maurice <thomas@maurice.fr>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
"""

from utils import setup_logger
import ConfigParser
import dns.tsigkeyring
import dns.query
import dns.update
import dns.zone
import base64
import uuid
import os

LOGGER = setup_logger("dnsbin")

CONFIG = ConfigParser.ConfigParser()
CONFIG.read('/etc/dnsbin.ini')

KEYRING = dns.tsigkeyring.from_text({
    CONFIG.get('key', 'name') : CONFIG.get('key', 'secret')
})

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

class Paste(object):
    def on_post(self, req, resp):
        update = dns.update.Update(
            CONFIG.get('server', 'zone'),
            keyring=KEYRING,
            keyalgorithm=CONFIG.get('key', 'algo')
        )

        body = req.context['json']['data']
        LOGGER.info("Received %d byte long paste" % len(body))
        try:
            body.decode("ascii")
        except UnicodeDecodeError:
            raise falcon.HTTPBadRequest("Your data is not ascii encoded !")

        uid = str(uuid.uuid4())
        i = 0
        for chunk in chunks(body, 254):
            i += 1
            LOGGER.info("Registering chunk %d of paste %s" % (i, uid))
            update.replace("%d.%s" % (i, uid), 10, 'TXT',str(chunk))
            response = dns.query.tcp(update, CONFIG.get('server', 'address'))
        LOGGER.info("Registering chunk number of paste %s" % uid)
        update.replace("%s" % uid, 10, 'TXT', "%d" % i)
        response = dns.query.tcp(update, CONFIG.get('server', 'address'))
        req.context['result'] = {"paste": uid}
        LOGGER.info("Paste %s registered !" % uid)
