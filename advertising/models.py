import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AdType(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    name = models.CharField(max_length=255, verbose_name='Идентификатор')
    template = models.CharField(max_length=255, verbose_name='Путь до шаблона')

    class Meta:
        # (блок, строка title, title + description)
        # только description
        unique_together = ('name',)
        verbose_name = 'Тип рекламы'
        verbose_name_plural = 'Тип рекламы'

    def __str__(self):
        return self.title


class AdAlign(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    align = models.CharField(max_length=255, verbose_name='Расположение')

    class Meta:
        # где располагается ( слева, справа, снизу, сверху, в определенном секторе)
        verbose_name = 'Расположение рекламы'
        verbose_name_plural = 'Расположение рекламы'

    def __str__(self):
        return self.title


class AdPage(models.Model):
    # где показывается? (на всех страницах, на конкретном выпуске)
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.CharField(max_length=255, verbose_name='Ссылка')
    additional = models.CharField(max_length=255, verbose_name='Дополнительные параметры ссылки', blank=True, null=True)

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
        verbose_name = 'Страницы рекламы'
        verbose_name_plural = 'Страницы рекламы'

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
        to_remove = []
        for ad in ads:
            for ad_page in ad.pages.all():
                if ad_page.url == page_url:
                    break
            else:
                to_remove.append(ad.id)
        ads = ads.exclude(id__in=to_remove)
    return ads


class Advertising(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    active = models.BooleanField(verbose_name='Активен', default=True)
    description = models.TextField(verbose_name='Текст рекламы')
    type = models.ForeignKey(AdType, verbose_name='Тип')
    align = models.ForeignKey(AdAlign, verbose_name='Расположение')
    pages = models.ManyToManyField(AdPage, verbose_name='Страницы')

    start_date = models.DateField(verbose_name=_('Start date'), default=datetime.datetime.today)
    end_date = models.DateField(verbose_name=_('End date'),
                                default=week_delta)

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'

    def __str__(self):
        return self.name
