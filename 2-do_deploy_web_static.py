#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers, using do_deploy.
"""
from fabric.api import put, run, env
from os.path import exists

# Utiliser les adresses IP fournies pour les serveurs
env.hosts = ['34.224.62.139', '100.25.119.231']  

def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive
        put(archive_path, '/tmp/')

        # Extract file name and prepare directory paths
        file_name = archive_path.split("/")[-1]
        file_wo_ext = file_name.split(".")[0]
        full_dir_path = "/data/web_static/releases/" + file_wo_ext + "/"

        # Commands to deploy the archive
        run("mkdir -p " + full_dir_path)
        run("tar -xzf /tmp/" + file_name + " -C " + full_dir_path)
        run("rm /tmp/" + file_name)
        mv_cmd = "mv " + full_dir_path + "web_static/* " + full_dir_path
        run(mv_cmd)
        run("rm -rf /data/web_static/current")
        run("ln -s " + full_dir_path + " /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception:
        return False

