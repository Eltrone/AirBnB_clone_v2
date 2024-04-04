#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo."""
from fabric.api import local
from datetime import datetime

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        # Get the current time in the specified format
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")
        # Create the archive file name
        archive_path = "versions/web_static_{}.tgz".format(now)
        # Create the archive using tar command
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None
