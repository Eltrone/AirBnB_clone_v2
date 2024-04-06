#!/usr/bin/python3
"""Un module pour distribuer une archive aux serveurs et la déployer"""
from fabric.api import put, run, env
import os

env.hosts = ['52.23.177.252', '18.204.7.7']
env.user = "ubuntu"

def do_deploy(archive_path):
    """Fonction pour déployer l'archive"""
    if not os.path.exists(archive_path):
        return False
    
    try:
        aname = os.path.basename(archive_path)
        rname = aname.split(".")[0]
        
        # Transférer l'archive vers le dossier /tmp/ du serveur
        put(archive_path, "/tmp/")
        
        # Décompresser l'archive dans /data/web_static/releases/
        run(f"mkdir -p /data/web_static/releases/{rname}")
        run(f"tar -xzf /tmp/{aname} -C /data/web_static/releases/{rname}/")
        
        # Supprimer l'archive du serveur
        run(f"rm /tmp/{aname}")
        
        # Supprimer le lien symbolique actuel et en créer un nouveau
        run("rm -rf /data/web_static/current")
        run(f"ln -s /data/web_static/releases/{rname}/ /data/web_static/current")
        
        # Nettoyage: déplacer les fichiers de web_static vers le dossier parent et supprimer web_static
        run(f"mv /data/web_static/current/web_static/* /data/web_static/current/")
        run("rm -rf /data/web_static/current/web_static")
        
        print("New version deployed!")
        return True
    except:
        return False
