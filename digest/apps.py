# -*- coding: utf-8 -*-
from django.apps import AppConfig

from conf.utils import likes_enable


class Config(AppConfig):
    name = 'digest'
    verbose_name = 'Дайджест'

    def ready(self):
        if likes_enable():
            import secretballot

            from .models import Item

            secretballot.enable_voting_on(Item)
