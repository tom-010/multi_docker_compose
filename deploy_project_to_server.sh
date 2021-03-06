#!/bin/bash


# exit 1 on error
set -e 


# Check/Process the given args
if [ -z "$2" ]
  then
    echo "No SSH-Connection given."
    echo "Call like: $0 sshuser@sshhost project_path"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ssh=$1
relative_project_path=$2
project_path=$(realpath $relative_project_path)
project_path=$(echo $project_path | sed 's:/*$::') # remove trailing /
project_name=$(basename $project_path)
user=$(echo $ssh | cut -d "@" -f 1)
host=$(echo $ssh | cut -d "@" -f 2)

# ensure that ansible is installed
if [ $(dpkg-query -W -f='${Status}' ansible 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    echo "Ansible is not installed yet. Install it now."
    sudo apt-get install -y ansible;
fi

# Add ssh credentials to server
if ssh -o PasswordAuthentication=no  -o BatchMode=yes $ssh exit &>/dev/null; then
    echo "SSH-Key already uploaded"
else
    echo "Uploading SSH-Key"
    ssh-copy-id $ssh || exit 1
fi

# Initialize/Prepare Server if not already done
if ssh $ssh 'test -f ~/init.py'; then
    # the server is already initalized
    echo "Server already initialized"
else
    echo "Initialize Server"
    ansible-playbook  $SCRIPT_DIR/ansible/prepare_server.yml -v -i $ssh,
fi


# adding project to the server
ansible-playbook  $SCRIPT_DIR/ansible/add_project.yml -v -e project_path=$project_path -e project_name=$project_name -i $ssh,