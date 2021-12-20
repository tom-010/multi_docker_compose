Multi Docker Compose
====================


## Motivaton

We want to deploy multiple projects on the same server, each
has it's own domain and and the infrastructure is defined via a
docker-compose-file. Each docker-compose file onloy exposes one
port of a project-specific reverse proxy. These projects are 
freely movable between servers. 


## Idea

The idea, that there is a two-level reverse-proxy system. On the 
first level, the traffic gets distributed by domain-name to the 
respective docker-compose project. There a project-specific reverse
proxy further distributes the traffic to the docker-containers by 
subdomain. 

## Getting started

Add this to your `/etc/hosts`:
```
127.0.0.1   system1.domain1.com
127.0.0.1   system2.domain1.com
127.0.0.1   system1.domain2.com
127.0.0.1   system2.domain2.com
```

## Setting up the firewall

Every project has to use an open port as docker does not allow socket 
communication. But we don't want to expose them to the internet. Thus 
we have to set up the firewall to protect these ports.