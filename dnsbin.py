#!/usr/bin/env python

"""
You do need to issue the following command first :
 $ pip install requests dnspython clifactory

Then to paste a file to a server :
$ ./dnsbin.py post 172.17.42.1 dnsbin.py
adaf1b42-cf03-4e12-aa17-c788b200047a

And there you go, you juste pasted this commandline :)

And to retrieve it :
$ ./dnsbin.py get 172.17.42.1 adaf1b42-cf03-4e12-aa17-c788b200047a
Paste is 8 chunks long
 * Getting 1.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
 * Getting 2.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
 * Getting 3.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
 * Getting 4.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
 * Getting 5.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
 * Getting 6.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
 * Getting 7.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
 * Getting 8.adaf1b42-cf03-4e12-aa17-c788b200047a chunk
Your paste :
 .... The file you juste pasted ! ...

 Easy isn't it ?

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

from clifactory import CommandLineInterface, Argument
import dns.resolver
import argparse
import requests
import socket
import base64
import json

cli = CommandLineInterface()

@cli.endpoint(
    Argument('server', metavar='ADDR', type=str, help="Server to push onto"),
    Argument('file', metavar='FILE', type=str, help="File to upload")
)
def do_post(args):
    f = open(args.file, 'r')
    data = f.read()
    f.close()
    try:
        data.decode('ascii')
    except UnicodeDecodeError:
        print "Data is not ASCII, encoding it into base 64"
        data = base64.b64encode(data)
    resp = requests.post("http://%s/paste" % args.server, json={"data": data})
    print resp.json()['data']['paste']

@cli.endpoint(
    Argument('server', metavar='ADDR', type=str, help="Server to retrieve from"),
    Argument('paste', metavar='UUID', type=str, help="Paste to get"),
    Argument('--decode', action='store_true', help="Do we have to decode the value ?")
)
def do_get(args):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [socket.gethostbyname(args.server)]
    answer = resolver.query("%s.paste" % args.paste, 'TXT')
    size = 0
    for data in answer:
        print data
        size = int(str(data).replace("\"", ""))
    print "Paste is %d chunks long" % size
    data = ""
    for chunk_id in range(1, size+1):
        print " * Getting %d.%s chunk" % (chunk_id, args.paste)
        answer = resolver.query("%d.%s.paste" % (chunk_id, args.paste), 'TXT')
        for chunk in answer:
            data += str(chunk)
    print "Your paste :\n"
    if args.decode:
        print base64.b64decode(data)
    else:
        print data

args = cli.parser.parse_args()
args.func(args)
