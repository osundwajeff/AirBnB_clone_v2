#!/usr/bin/python3
"""Fabric script that generates a .tgz archive
from the contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack"""

from datetime import datetime
from fabric.api import local, put, run, env
import os

env.hosts = ['3.236.238.180', '3.236.109.232']
env.user = "ubuntu"
env.key = "~/.ssh/id_rsa"


def do_pack():
    """packs web static to tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None

def do_deploy(archive_path):
    """Deploys archive to web servers"""
    if not os.path.exists(archive_path) and not os.path.isfile(archive_path):
        return False

    temp = archive_path.split('/')
    temp0 = temp[1].split(".")
    f = temp0[0]

    try:
        put(archive_path, '/tmp')
        run("sudo mkdir -p /data/web_static/releases/" + f + "/")
        run("sudo tar -xzf /tmp/" + f + ".tgz" +
            " -C /data/web_static/releases/" + f + "/")
        run("sudo rm /tmp/" + f + ".tgz")
        run("sudo mv /data/web_static/releases/" + f +
            "/web_static/* /data/web_static/releases/" + f + "/")
        run("sudo rm -rf /data/web_static/releases/" + f + "/web_static")
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/" + f +
            "/ /data/web_static/current")
        return True
    except:
        return False

    return True
