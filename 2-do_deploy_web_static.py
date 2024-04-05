#!/usr/bin/python3
""" distributes an archive to your web servers """

from fabric.api import *
from os import path

env.user = 'ubuntu'
env.hosts = ["34.224.62.139", "100.25.119.231"]
env.key_filename = "~/.ssh/id_rsa"

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not path.exists(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    foldername = '/data/web_static/releases/' + filename.split('.')[0]

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(foldername))
        run("tar -xzf /tmp/{} -C {}".format(filename, foldername))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}".format(foldername, foldername))
        run("rm -rf {}/web_static".format(foldername))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(foldername))
        print("New version deployed!")
        return True
    except:
        return False
