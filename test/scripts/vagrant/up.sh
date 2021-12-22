#!/bin/bash

# 1. create the machine
vagrant up || exit 1

# 2. ssh preperation: remove old known host, first connection to accecpt, copy up my key
SSH_USER=vagrant
SSH_HOST=192.168.33.10
SSH_PASSWORD='vagrant'
ssh-keygen -R $SSH_HOST
sshpass -p $SSH_PASSWORD ssh -o StrictHostKeyChecking=no $SSH_USER@$SSH_HOST "echo 'ssh ok'"
echo $SSH_PASSWORD | sshpass ssh-copy-id $SSH_USER@$SSH_HOST > /dev/null
