# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import os

from django.core.management.base import BaseCommand
from allmychanges.api import search_category, track_changelog, get_changelogs
from allmychanges.config import read_config

from conf.settings import BASE_DIR


def subscribe_all_python():
    config_path = os.path.join(BASE_DIR, 'allmychanges.cfg')
    assert os.path.exists(config_path)
    config = read_config(config_path)

    section = 'python'

    changelogs = get_changelogs(config, tracked=True)
    subscribed_packages = [x['name'] for x in changelogs
                           if 'namespace' in x and x['namespace'] == section]

    python_libraries = search_category(config, section)

    all_cnt = len(python_libraries)

    for i, x in enumerate(python_libraries):
        if i % 10 == 0:
            print("Process: %s of %s" % (i, all_cnt))

        if not (x.get('name') in subscribed_packages):
            print("Track: ", x.get('name'))
            track_changelog(config, x)


class Command(BaseCommand):
    args = 'no arguments!'
    help = u'News import from external resources'

    def handle(self, *args, **options):
        """
        Основной метод - точка входа
        """
        subscribe_all_python()
