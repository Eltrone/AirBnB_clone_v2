#!/usr/bin/python3
""" distributes an archive to your web servers """

from fabric.api import env
from fabric.api import put
from fabric.api import run
import os.path

env.user = 'ubuntu'
env.hosts = ["34.224.62.139", "100.25.119.231"]
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """ do_deploy fonction """
    if os.path.exists(archive_path) is False:
        return False
    try:
        arc = archive_path.split("/")
        base = arc[1].strip('.tgz')
        put(archive_path, '/tmp/')
        sudo('mkdir -p /data/web_static/releases/{}'.format(base))
        main = "/data/web_static/releases/{}".format(base)
        sudo('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))
        sudo('rm /tmp/{}'.format(arc[1]))
        sudo('mv {}/web_static/* {}/'.format(main, main))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ "/data/web_static/current"'.format(main))
        return True

    except:
        return False
