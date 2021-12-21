./scripts/vagrant/up.sh
./scripts/ansible/prepare_server.sh
./scripts/ansible/configure_and_start.sh
./scripts/test.sh || exit 1
./scripts/vagrant/destroy.sh