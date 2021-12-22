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
192.168.33.10   system1.domain1.com
192.168.33.10   system2.domain1.com
192.168.33.10   alternative1.domain1.com
192.168.33.10   system1.domain2.com
192.168.33.10   system2.domain2.com
```

To run everything end to end, read and run: 
```bash
cd test
./scripts/up_test_down.sh
```

## Steps

There are essentially two steps:
1. Prepare the multi-project server
2. Add the project to the multi-project server
   1. Upload the files
   2. Reinitialize


This can be turned inside out. Thus when you created a new project you 
provide a user@location. The prepare-server script then checks if the 
multi-project server is already set up and if not does so. Then it adds
the current project to the given server.


## Todo

* Zero-Downtime when reinitialize