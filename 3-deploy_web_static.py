#!/usr/bin/python3
"""
Empaqueter le contenu statique et le déployer sur le serveur.
"""

from fabric.api import local, put, run, env
from datetime import datetime
import os

env.hosts = ["34.224.62.139", "100.25.119.231"]


def do_pack():
    """Empaqueter le contenu statique et le déployer sur le serveur."""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distribue une archive aux serveurs web."""
    if not os.path.exists(archive_path):
        return False
    try:
        archive_filename = archive_path.split("/")[-1]
        without_ext = archive_filename.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(without_ext)
        put(archive_path, '/tmp/')
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))
        run("rm /tmp/{}".format(archive_filename))
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Crée et distribue une archive aux serveurs web."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
