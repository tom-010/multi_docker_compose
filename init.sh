#!/bin/bash
export $(cat .env | xargs)
python3 init.py $PROJECT_PATH