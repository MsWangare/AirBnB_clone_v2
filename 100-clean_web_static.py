#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the contents
# of the web_static folder of your AirBnB Colne repo,
# using the function do_pack
from datetime import datetime
from fabric.api import local
from fabric.api import *
from os.path import isfile

env.user = 'ubuntu'
env.hosts = ['34.75.217.72', '34.73.33.136']


def do_pack():
    """
    that fenerates a .tgz archive from the contents of the web_static folder
    """
    dt = datetime.now()
    file = 'web_static' + str(dt.year) + str(dt.month) + str(dt.day)
    file = file + str(dt.hour) + str(dt.minute) + str(dt.second) + '.tgz'
    local('mkdir -p versions')
    directory = local('tar -cvzf versions/{} web_static'. format(file))
    if directory.failed:
        return None
    return 'versions/{}'.format(file)


def do_deploy(archive_path):
    """
    Fabric script (based on the file 1-pack_web_static.py)
    that distributes an archive to your web servers, using
    the function do_deploy:
    """
    if not isfile(archive_path):
        return False
    put(archive_path, '/tmp/')
    file = archive_path.replace('.tgz', '')
    file = file.replace('versions/', '')
    run('mkdir -p /data/web_static/releases/{}/'.format(file))
    run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
        .format(file, file))
    run('rm /tmp/{}.tgz'.format(file))
    run('mv /data/web_static/releases/{}/web_static/* '.format(file) +
        '/data/web_static/releases/{}/'.format(file))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(file))
    run('rm -rf /data/web_static/current')
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
        .format(file))
    print('New version deployed!')
    return True


def deploy():
    """
    Fabric script (based on the file 2-do_deploy_web_static.py)
    that creates and distributes an archive to your web servers,
    using the function deploy:
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Fabric script (based on the file 3-deploy_web_static.py)
    that deletes out-of-date archives, using the function
    do_clean:
    """
    try:
        number = int(number)
    except:
        return None
    if number < 0:
        return None
    number = 2 if (number == 0 or number == 1) else (number + 1)
    with lcd("./versions"):
        local('ls -t | tail -n +{:d} | xargs rm -rf --'.format(number))
    with cd("/data/web_static/releases"):
        run('ls -t | tail -n +{:d} | xargs rm -rf --'.format(number))
