#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ["34.224.62.139", "100.25.119.231"]

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False
    try:
        # Upload the archive
        put(archive_path, '/tmp/')
        archive_filename = archive_path.split("/")[-1]
        without_ext = archive_filename.split(".")[0]
        release_path = f"/data/web_static/releases/{without_ext}/"
        # Uncompress the archive
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf /tmp/{archive_filename} -C {release_path}")
        run(f"rm /tmp/{archive_filename}")
        # Move the content to the correct location
        run(f"mv {release_path}web_static/* {release_path}")
        run(f"rm -rf {release_path}web_static")
        # Delete the current symbolic link and create a new one
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")
        print("New version deployed!")
        return True
    except:
        return False
