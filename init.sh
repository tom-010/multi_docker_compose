#!/bin/bash
mkdir -p conf/reverse_proxy/conf.d 2> /dev/null
export $(cat .env | xargs)
python3 init.py $PROJECT_PATH