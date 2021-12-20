import argparse
from os import listdir
from os.path import isdir, join, isfile



parser = argparse.ArgumentParser(description='Configure the reverse-proxy for multiple docker-compose projects')
parser.add_argument('path', help='Path to the folder that contains the projects as folders')
args = parser.parse_args()


def is_project(root, project_name):
    directory = join(root, project_name)
    if not isdir(directory):
        return False
    if isfile(join(directory, 'docker-compose.yaml')):
        return True
    if isfile(join(directory, 'docker-compose.yml')):
        return True
    return False


candidates = [f for f in listdir(args.path) if is_project(args.path, f)]
print(candidates)