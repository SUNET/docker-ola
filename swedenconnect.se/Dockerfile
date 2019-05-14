FROM nrpe-common:latest
RUN apt-get -y install jq opensaml2-tools xmlsec1
ADD ola.yaml /etc/
COPY plugins/ /usr/lib/nagios/plugins/
ADD swedenconnect-signer.crt /etc/ssl/certs/
