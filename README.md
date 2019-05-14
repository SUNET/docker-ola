OLA NPRE containers
====

This repo contains a set of docker containers corresponding to OLA definitions of Sunet services. Build and push all containers using the Makefile ("make").

Structure of an OLA NPRE container
---

Each container should inherit from docker-nrpe-common and add any additional "stuff" needed to monitor that service. For instance:

```
FROM nrpe-common:latest
ADD check-some-service.sh /usr/lib/nagios/plugins/
```

Note that the container MUST define the name of the service as an environment variable `OLA_NAME`. In addition each container MUST supply a yaml file containing service and servicegroup definitions: `/etc/ola.yaml` with the following structure:

```
name: the_awsome_collection_of_services
services:
   - a_service:
      name: "A Service That Check in the OLA"
      command: "/usr/lib/nagios/plugins/check-some-service.sh some arguments"
servicegroups:
   - a_group:
      members: ["a_service_name"]
```

The base container (nrpe-common) has an entrypoint (that should not be changed) which starts nrpe on port 5666. When starting the container, map this to a unique port on the host and provide that port as environment variable `OLA_PORT`. Optionally also override `OLA_HOSTNAME` and deploy the container separately from the nagios host. The container SHOULD map the `/etc/nagios3` directory where nagios configuration (according to deb/ubuntu layout) for the service checks are written at container startup.

The typical launch command looks something like this:

```
docker run -p 56661:5666 -v /etc/nagios3:/etc/nagios3 the_awsome_collection_of_services:latest
```

A similar example is provided in docker-compose.yaml
