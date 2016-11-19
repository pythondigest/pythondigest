# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class Config(AppConfig):
    name = 'frontend'
    verbose_name = _('Frontend')
