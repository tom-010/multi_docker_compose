#!/bin/bash

ansible-playbook -i ansible/inventory ansible/prepare_server.yml -v
