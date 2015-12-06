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
import traceback

def error_handler(exce, req, resp, params):
    if issubclass(exce.__class__, falcon.HTTPError):
        resp.status = exce.status
        req.context['result'] = {'error': "%s: %s" % (exce.title, exce.description)}
    else:
        print traceback.print_exc()
        resp.status = falcon.HTTP_500
        req.context['result'] = {'error': str(traceback.format_exc())}
