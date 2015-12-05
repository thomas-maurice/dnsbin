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

import sys
import os
import falcon
import json

class JSONInput(object):
    def process_request(self, req, resp):
        if req.method in ['GET', 'HEAD', 'OPTIONS']:
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')
        try:
            req.context['json'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError) as exce:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

class JSONOutput(object):
    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps({'status': int(resp.status.split(' ')[0]),
            'data': req.context['result']
        })
