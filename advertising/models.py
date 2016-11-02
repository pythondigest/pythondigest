# -*- encoding: utf-8 -*-
import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AdType(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    name = models.CharField(max_length=255, verbose_name=_('ID'))
    template = models.CharField(max_length=255, verbose_name=_('Template'),
                                help_text=_('Path to template'))

    class Meta:
        unique_together = ('name',)
        verbose_name = _('Ads type')
        verbose_name_plural = _('Ads types')

    def __str__(self):
        return self.title


class AdAlign(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    align = models.CharField(max_length=255, verbose_name=_('Align'))

    class Meta:
        verbose_name = _('Ads align')
        verbose_name_plural = _('Ads align')

    def __str__(self):
        return self.title


class AdPage(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.CharField(max_length=255, verbose_name=_('Slug'))
    additional = models.CharField(
        max_length=255,
        verbose_name=_('Additional info'),
        blank=True
    )

    @property
    def url(self):
        if self.additional:
            result = reverse(self.slug, kwargs=eval(self.additional))
        else:
            result = reverse(self.slug)
        return result

    def clean(self):
        try:
            __ = self.url
        except NoReverseMatch:
            raise ValidationError(_('Not valid slug for AdPage'))
        super(AdPage, self).clean()

    class Meta:
        verbose_name = _('Ads page')
        verbose_name_plural = _('Ads pages')

    def __str__(self):
        return self.title


def week_delta():
    return datetime.datetime.now() + datetime.timedelta(days=7)


def get_ads(page_url=None):
    ads = Advertising.objects.filter(
        start_date__lte=datetime.datetime.now(),
        end_date__gte=datetime.datetime.now(),
        active=True,
        # можно как-то сюда же запихать нижнюю логику?
    )

    if page_url is not None:
        ads = ads.filter(pages__url=page_url)
        # to_remove = []
        # for ad in ads:
        #     for ad_page in ad.pages.all():
        #         if ad_page.url == page_url:
        #             break
        #     else:
        #         to_remove.append(ad.id)
        # ads = ads.exclude(id__in=to_remove)
    return ads


class Advertising(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    description = models.TextField(verbose_name=_('Description'))
    type = models.ForeignKey(AdType, verbose_name=_('Ads type'))
    align = models.ForeignKey(AdAlign, verbose_name=_('Ads align'))
    pages = models.ManyToManyField(AdPage, verbose_name=_('Ads pages'))

    start_date = models.DateField(
        verbose_name=_('Start date'),
        default=datetime.datetime.today
    )
    end_date = models.DateField(
        verbose_name=_('End date'),
        default=week_delta
    )

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'

    def __str__(self):
        return self.name
