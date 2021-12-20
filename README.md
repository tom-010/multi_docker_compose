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

