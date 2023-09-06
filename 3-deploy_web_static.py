#!/usr/bin/python3
"""
Distributes an archive to my web servers"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['52.87.153.92', '52.205.84.52']
env.user = 'ubuntu'


def deploy():

    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


def do_pack():

    try:
        local('mkdir -p versions')
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))
        local('tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    
    if not os.path.exists(archive_path):
        return False
    file_name = archive_path.split('/')[1]
    file_path = '/data/web_static/releases/'
    releases_path = file_path + file_name[:-4]
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(releases_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, releases_path))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}/'.format(releases_path, releases_path))
        run('rm -rf {}/web_static'.format(releases_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')
        return True
    except:
        return False
