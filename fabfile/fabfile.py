# -*- coding: utf-8 -*-
#
import os

from fabric.api import *

PROJECT_FOLDER = '/home/pythondigest/pythondigest.ru/'
REPO_FOLDER = os.path.join(PROJECT_FOLDER, 'repo')
ENV_FOLDER = os.path.join(PROJECT_FOLDER, 'env')
ENV_PATH = os.path.join(ENV_FOLDER, 'bin/activate')


def pull():
    with cd(REPO_FOLDER):
        run('git pull')


def deploy():
    pull()
    update_libs()
    migrate()
    static()
    restart()


def update_libs():
    with prefix('source %s' % ENV_PATH):
        with cd(REPO_FOLDER):
            run('pip install -r requirements.txt')


def restart():
    sudo('service uwsgi restart')


def migrate():
    with prefix('source %s' % ENV_PATH):
        with cd(REPO_FOLDER):
            run('python manage.py migrate --noinput')


def static():
    with prefix('source %s' % ENV_PATH):
        with cd(REPO_FOLDER):
            run('python manage.py collectstatic --noinput')
