./scripts/vagrant/up.sh

./deploy_project_to_server.sh vagrant@192.168.33.10 ./test/projects/domain1.com
./deploy_project_to_server.sh vagrant@192.168.33.10 ./test/projects/domain2.com

./scripts/test.sh || exit 1
./scripts/vagrant/destroy.sh