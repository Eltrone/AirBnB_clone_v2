#!/usr/bin/python3
"""
Nettoie les archives obsolètes localement et sur les serveurs.
"""

from fabric.api import *

env.hosts = ["34.224.62.139", "100.25.119.231"] 
env.user = "ubuntu"  # Utilisateur pour les connexions SSH


def do_clean(number=0):  # Corrige E302 en ajoutantligne vide supplémentaire
    """
    Garde seulement les 'number' archives les plus récentes.
    """
    number = int(number)
    if number in [0, 1]:
        number = 1  # Par défaut ou si 1, garder la plus récente
    else:
        number += 1  # Garder 'number' archives

    # Nettoyer localement dans 'versions', divisé pour corriger E501
    local("ls -t versions/web_static_* | tail -n +{} | "
          "xargs rm -rf".format(number))

    # Nettoyer sur les serveurs '/data/web_static/releases', divisé pour E501
    run("ls -t /data/web_static/releases/web_static_* | tail -n +{} | "
        "xargs rm -rf".format(number))
