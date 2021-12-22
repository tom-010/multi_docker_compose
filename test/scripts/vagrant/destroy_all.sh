#!/bin/bash
set -e 
vagrant box list | cut -f 1 -d ' ' | xargs -L 1 vagrant box remove -f
vagrant global-status --prune