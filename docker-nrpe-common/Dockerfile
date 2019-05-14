FROM debian:stable
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections 
RUN apt-get -q update && apt-get -y upgrade && apt-get -y install nagios-nrpe-server python3-pip wget curl python3-dev python3-openssl locales
RUN pip3 install nagios-api diesel greenet
RUN mkdir -p /etc/nrpe.d
ADD nrpe.cfg /etc/nrpe.cfg
ADD entrypoint.sh /entrypoint.sh
ADD generate-config.py /generate-config.py
COPY plugins/ /usr/lib/nagios/plugins/
RUN echo "sv_SE.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
ENV LANG sv_SE.UTF-8
ENV LANGUAGE sv_SE:sv
ENV LC_ALL sv_SE.UTF-8
EXPOSE 5666
VOLUME /etc/nagios3/conf.d
ENTRYPOINT ["/entrypoint.sh"]
