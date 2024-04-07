#!/usr/bin/python3
"""
Distribue une archive à vos serveurs web
"""

from fabric.api import env, put, run
import os.path

env.user = 'ubuntu'
env.hosts = ["34.224.62.139", "100.25.119.231"]
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    Déploie l'archive sur les serveurs
    """
    if not os.path.exists(archive_path):
        return False
    try:
        arc = archive_path.split("/")
        base = arc[1].strip('.tgz')
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}'.format(base))
        main = "/data/web_static/releases/{}".format(base)
        run('tar -xzf /tmp/{} -C {}/'.format(arc[1], main))
        run('rm /tmp/{}'.format(arc[1]))
        run('mv {}/web_static/* {}/'.format(main, main))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ "/data/web_static/current"'.format(main))
        return True

    except:
        return False
