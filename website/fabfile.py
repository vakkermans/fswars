from fabric.api import *
from fabric.contrib.files import put, exists, append

env.user = 'vakkermans'
env.hosts = ['109.169.40.165'] # ['freesoundwars.com']

PROJECT_NAME = 'fswars'

SRC_DIR = 'src/%s/website/' % PROJECT_NAME
DATA_DIR = "data/%s/" % PROJECT_NAME

GIT_REP = 'git://github.com/vakkermans/fswars.git'

VIRTUALENV_ACTIVATE = '~/.virtualenvs/fswars/bin/activate'

def clearpyc():
    with cd(SRC_DIR):
        run("find . -name \"*.pyc\" -delete")


def syncdb():
    with cd(SRC_DIR):
        run('source ~/.virtualenvs/%s/bin/activate && python manage.py syncdb' % PROJECT_NAME)


def deletedb():
    db_path = "data/%s/%s.db" % (PROJECT_NAME, PROJECT_NAME)
    if exists(db_path):
        run("rm %s" % db_path)
    else:
        print 'WARNING: could not find db file'


def stop():
    sudo("supervisorctl stop %s" % PROJECT_NAME, shell=False)


def start():
    sudo("supervisorctl start %s" % PROJECT_NAME, shell=False)


def restart():
    sudo("supervisorctl restart %s" % PROJECT_NAME, shell=False)


def pull():
    with cd(SRC_DIR):
        run("git pull")


def reconf():
    with cd(SRC_DIR):
        run("cp settings_local.barcelona.py settings_local.py")


def redeploy():
    stop()
    pull()
    reconf()
    deletedb()
    syncdb()
    start()


def setup():
    run("mkdir -p %s" % DATA_DIR)
    run("mkdir -p %sdynamic_media" % DATA_DIR)

    if not exists(SRC_DIR):
        with cd("src/"):
            run("git clone %s" % GIT_REP)

    #crontab()


def dependencies():
    with cd('/tmp/'):
        run("""source %s && \
                pip install --upgrade \
                    django simplejson django-piston flup pika \
                    git+https://github.com/g-roma/freesound-python.git#egg=freesound""" % VIRTUALENV_ACTIVATE)

#def crontab():
#    run('crontab -l > /tmp/crondump')
#    append("/tmp/crondump", "*/1 * * * * PYTHONPATH=/home/vakkermans/src/twobbler-server DJANGO_SETTINGS_MODULE=\"settings\" /home/vakkermans/.virtualenvs/twobbler-server/bin/python /home/vakkermans/src/twobbler-server/utils/mail.py 2>&1")
#    #append("/tmp/crondump", "*/1 * * * * PYTHONPATH=/home/vakkermans/src/twobbler-server DJANGO_SETTINGS_MODULE=\"settings\" /home/vakkermans/.virtualenvs/twobbler-server/bin/python /home/vakkermans/src/twobbler-server/manage.py process_search_queue 2>&1")
#    run('crontab /tmp/crondump')
