# dnsbin
The most useless and under optimized pastebin ever known to mankind.

# Introduction
dnsbin is a pastebin based on DNS. It means that you
can submit a paste using a basic HTTP api, and
retrieving it via DNS requests.

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

# How does it work ?
The bind DNS server registers a "local" zone .paste that
he thinks he is rightful to authoritate on.

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
