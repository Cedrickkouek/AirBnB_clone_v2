from fabric.api import local, env, run, put
from datetime import datetime
import os

# Set the default hosts
env.hosts = ['xx-web-01', 'xx-web-02']

def do_pack():
    """Packs the web_static content into a .tgz archive"""
    try:
        now = datetime.now()
        file_name = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(file_name))
        return "versions/{}".format(file_name)
    except:
        return None

def do_deploy(archive_path):
    """Deploys the archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        file_name_no_ext = file_name.split(".")[0]
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p /data/web_static/releases/{}/".format(file_name_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, file_name_no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(file_name_no_ext, file_name_no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static".format(file_name_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(file_name_no_ext))
        return True
    except:
        return False

def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
