# dnsbin
The most useless and under optimized pastebin ever known to mankind.

# Introduction
dnsbin is a pastebin based on DNS. It means that you
can submit a paste using a basic HTTP api, and
retrieving it via DNS requests.

## What's the concept ?
The concept is quite simple, it uses the DNS protocol (and more especially the TXT
data field) to store any arbitrary data. This is silly but also interesting since
DNS has to be the less filtered protocol ever (unless you live in China, lol) and
benefits from la native caching system. 

That means you virtually have a free CDN :) (Eventough this functionnality has not
been developped yet, see TODO)

It has initially be developped to be some kind of under-optimized pastebin system but since
you can store any ASCII data in TXT fields, you can upload base64 encoded binary files
if you want. Bittorrent is dead :D

(or not.)

## Why would you do that ?
Because I could :3

# How to install it ?
Just build the Dockerfile :
```bash
docker build -t dnsbin .
```
And run it :
```bash
./start_dnsbin.sh
```

And you're done !

# Using the commandline
To use the command line you need to install few packages using pip :
```bash
pip install requests dnspython clifactory
```
## Posting a file
```bash
./dnsbin.py post someserver.tld file_name
87597b44-d913-4740-9091-d9bd62b8f422
```

Done ! Your paste has id `87597b44-d913-4740-9091-d9bd62b8f422`

## Getting a paste
```bash
./dnsbin.py get someserver.tld 87597b44-d913-4740-9091-d9bd62b8f422
Paste is 15 chunks long
 * Getting 1.87597b44-d913-4740-9091-d9bd62b8f422 chunk
 * Getting 2.87597b44-d913-4740-9091-d9bd62b8f422 chunk
  ... Some more chunks ...
 * Getting 14.87597b44-d913-4740-9091-d9bd62b8f422 chunk
 * Getting 15.87597b44-d913-4740-9091-d9bd62b8f422 chunk
Your paste :
 ... The text you did paste ! ...
```

That was easy :)

# Customizing it
You can customize the docker setting up some parameters in the startup script.
Currently the only one you can play with is the TSIG key used to update the server
which I actually advise you to change if you plan on putting the server online.
You can generate a new key via
```bash
dnssec-keygen -a HMAC-SHA512 -b 512 -r /dev/urandom -n HOST keyname
```

If you don't, anyone could push updates to your zone.

# How does it work under the hood ?
The bind DNS server registers a "local" zone .paste that
he thinks he is rightful to authoritate on.

I don't quite think that in the current implementation
fqdn chunks are supported, but let me know if you find
a way to do it, I'll try to implement it sometime !

The HTTP API uses TSIG keys to post update to the zone
everytime you want to get a paste. The paste is encoded
with base64 and chunked into pieces to fit into the TXT
fields of the DNS.

Then for each post you get *uuid.paste* which contains
the number of chunks the paste has, and then *1.uuid*,
*2.uuid* ... *N.uuid* containing each chunk.

That is almost as stupid as simple :)

# TODO
 * Support "fqdn pastes", that will allow you to
   query Google's own 8.8.8.8 for *someuuid*.yourdomain.com :)
 * DNSSEC \o/
 * Add a pastes.paste endpoint listing all the pastes
 * Add a mechanism to purge old pastes
 * Add a way to parallelize upload
 * Accept only ASCII data posts, so that the encoding is
   deported client side
 * Support to chunk big content into multiple pastes and store
   the references of this pastes in the "master paste"
 * Add some metadata to the pastes somehow
