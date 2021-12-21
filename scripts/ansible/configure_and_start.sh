#!/bin/bash

ansible-playbook -i ansible/inventory ansible/configure_and_start.yml -v
