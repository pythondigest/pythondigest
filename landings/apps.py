# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LandingsConfig(AppConfig):
    name = 'landings'
    verbose_name = _("Landings")
