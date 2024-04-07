#!/usr/bin/python3
"""
    Empaqueter le contenu statique et le déployer sur le serveur.
"""
import time
from fabric.context_managers import cd
from fabric.api import local
from fabric.api import get
from fabric.api import put
from fabric.api import reboot
from fabric.api import run
from fabric.api import sudo
from fabric.api import env
import os.path
# do_pack = __import__('1-pack_web_static').do_pack
# do_deploy = __import__('2-do_deploy_web_static').do_deploy
env.hosts = ["34.224.62.139", "100.25.119.231"]  


def do_pack():
    """ Empaqueter le contenu statique"""
    try:
        if not os.path.exists('versions'):
            l = local("mkdir -p versions")
        n = "versions/web_static_{}.tgz".\
            format(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
        o = local("tar -cvzf {} web_static".format(n))
        # x = local("mv {} versions".format(n))
        # p = local("pwd {}".format(n))
        # return 'versions/{}'.format(n)
        return n
    except:
        return None


def do_deploy(archive_path):
    """ Déployer mon archive tgz sur mes serveurs. """
    try:
        put(archive_path, '/tmp/')
        c1 = 'mkdir -p /data/web_static/releases/{}/'
        run(c1.format(archive_path[9:-4]))
        c2 = 'tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
        run(c2.format(archive_path[9:], archive_path[9:-4]))
        run('rm /tmp/{}'.format(archive_path[9:]))
        c3 = 'mv /data/web_static/releases/{}/web_static/* \
              /data/web_static/releases/{}/'
        run(c3.format(archive_path[9:-4], archive_path[9:-4]))
        c4 = 'rm -rf  /data/web_static/releases/{}/web_static/'
        run(c4.format(archive_path[9:-4]))
        run('rm -rf /data/web_static/current')
        c5 = 'ln -s /data/web_static/releases/{}/ {}'
        run(c5.format(archive_path[9:-4], '/data/web_static/current'))
        return True
    except:
        return False


path = do_pack()


def deploy():
    """ Empaqueter et déployer """
    if path:
        return do_deploy(path)
    else:
        return False
