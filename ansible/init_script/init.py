from task_in_steps import Step, run_steps
import argparse
from os import listdir
from os.path import isdir, join, isfile
import re
import os


def main():
    config = Config().parse_args()
    run_steps(config, [
        CreateFolderForNginxConf(),
        CleanupOldConfigurations(),
        CreateNewReverseProxyConfigurations(),
        CreateDockerComposeFile(),
        CreateUpScript(),
        CreateDownScript(),
    ])

class Config:

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Configure the reverse-proxy for multiple docker-compose projects')
        parser.add_argument('path', help='Path to the folder that contains the projects as folders')
        self.args = parser.parse_args()


        def is_project(root, project_name):
            directory = join(root, project_name)
            if not isdir(directory):
                return False
            if isfile(join(directory, 'docker-compose.yaml')):
                return True
            if isfile(join(directory, 'docker-compose.yml')):
                return True
            return False


        self.projects = [f for f in listdir(self.args.path) if is_project(self.args.path, f)]
        self.projects.sort()
        self.conf_dir = './conf/reverse_proxy/conf.d/'
        return self

    def clean_name(self, name):
        return re.sub('[^0-9a-zA-Z]+', '', name)

reverse_proxy_template = """

server {
    server_name {domains};

    location / {
        proxy_pass http://{project_name_clean}_reverse_proxy_1;
        proxy_set_header Host $host;
    }
}
"""

reverse_proxy_default_template = """
server {
    listen 80 default_server;
    server_name _;
    return 404;
}
"""

class CreateFolderForNginxConf(Step):

    def can_skip(self, config):
        return isdir(config.conf_dir)

    def run(self, config):
        os.system(f'mkdir -p {config.conf_dir} 2> /dev/null')
        return True


class CleanupOldConfigurations(Step):

    def run(self, config):
        for f in [ f for f in listdir(config.conf_dir) if f.endswith(".conf") ]:
            os.remove(os.path.join(config.conf_dir, f)) # cleanup
        return True


class CreateNewReverseProxyConfigurations(Step):

    def run(self, config):
        # step 1: collecting domains
        domains = self._search_projects_for_domains(config)
        self._generate_reverse_proxy_config(config, domains)
        self._generate_reverse_proxy_default_config(config)
        return True

    def _search_projects_for_domains(self, config):
        domains = {}
        for project in config.projects:
            project_domains = []
            conf_dir = config.conf_dir
            if conf_dir.startswith('./'):
                conf_dir = conf_dir[2:]
            
            path = join(config.args.path, project, conf_dir)
            for config_file in [ f for f in listdir(path) if f.endswith(".conf") ]:
                config_file = join(path, config_file)
                for group in [self._nginx_server_name_line_to_domains(line) for line in open(config_file).readlines() if 'server_name' in line]:
                    project_domains += group
            domains[project] = project_domains
        return domains

    def _nginx_server_name_line_to_domains(self, line):
        return line.replace('server_name', '').strip().split(';')[0].split(' ')

    def _generate_reverse_proxy_config(self, config, domains):
        for project in config.projects:
            content = reverse_proxy_template
            content = content.replace('{domains}', ' '.join(domains[project]))
            content = content.replace('{project_name_clean}', config.clean_name(project))
            with open(f'{config.conf_dir}{project}.conf', 'w') as file:
                file.write(content)

    def _generate_reverse_proxy_default_config(self, config):
        open(f'{config.conf_dir}default.conf', 'w').write(reverse_proxy_default_template)
        reverse_proxy_default_template




class CreateDockerComposeFile(Step):
    docker_compose_template = """version: '3.5'

services:

  reverse_proxy:
    image: nginx:1.21.4
    restart: unless-stopped
    ports:
      - 80:80
    volumes:
      - {conf_dir}:/etc/nginx/conf.d
      - /var/run/docker.sock:/tmp/docker.sock:ro
    networks:
{networks}

networks:
{network_definitions}

"""
    def run(self, config):
        networks = ''
        network_definitions = ''
        for project in config.projects:
            networks += f'      - {config.clean_name(project)}_reverse-proxy-net\n'
            network_definitions += f'  {config.clean_name(project)}_reverse-proxy-net:\n    external: true\n'

        docker_compose_content = self.docker_compose_template
        docker_compose_content = docker_compose_content.replace('{conf_dir}', config.conf_dir)
        docker_compose_content = docker_compose_content.replace('{networks}', networks)
        docker_compose_content = docker_compose_content.replace('{network_definitions}', network_definitions)
        with open('docker-compose.yaml', 'w') as f:
            f.write(docker_compose_content)
        return True



class CreateUpScript(Step):

    def run(self, config):
        up_script = 'ORIGINAL_PWD=$PWD\n'

        for project in config.projects:
            path = join(config.args.path, project)
            # we delete the ports section with yq on the fly and load the modified yaml via stdin
            up_script += f'cd {path}\n'
            up_script += f'yq e "del(.services.reverse_proxy.ports)" ./docker-compose.yaml | docker-compose -f - up --build -d > docker-compose-create.logs 2>&1\n'
            up_script += f'cd $ORIGINAL_PWD\n\n'
        up_script += '\ndocker-compose up -d\n'
        with open('up.sh', 'w') as f:
            f.write(up_script)
        os.system('chmod +x up.sh')
        return True


class CreateDownScript(Step):

    def run(self, config):
        down_script = 'ORIGINAL_PWD=$PWD\ndocker-compose down &\n'
        for project in config.projects:
            path = join(config.args.path, project)
            down_script += '\n'
            down_script += f'cd {path}\n'
            down_script += 'docker-compose down &\n'
            down_script += 'cd $ORIGINAL_PWD\n'
            down_script += '\n'
        with open('down.sh', 'w') as f:
            f.write(down_script)
        os.system('chmod +x down.sh')
        return True


        
if __name__ == "__main__":
    main()