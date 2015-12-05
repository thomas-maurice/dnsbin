FROM alpine:latest
MAINTAINER Thomas Maurice <thomas@maurice.fr>

RUN apk update && \
    apk add \
        bind \
        python \
        python-dev \
        py-pip

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir -p /var/run/named /templates /var/cache/bind
COPY bind/named.conf.options bind/named.conf /etc/bind/
RUN chown -R named:named /var/run/named /etc/bind/ /var/cache/bind
COPY templates/*.j2 update_scripts/*.j2 /templates/
COPY scripts/run.sh /run.sh
COPY api /usr/app/

EXPOSE 53 80

CMD /run.sh
