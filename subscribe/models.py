import uuid

from django.db import models


class Subscribers(models.Model):

    useremail = models.EmailField(
                    unique=True,
                    blank=False,
                    null=False,
                    max_length=75
    )
    subscribe = models.BooleanField(
                    default=True
    )
    id_subscriber = models.CharField(
                    max_length=50,
                    unique=True,
                    default=str(uuid.uuid4()).replace('-','')
    )
    #NOTE
    #add unsubscribe_link for mail


    class Meta:
        verbose_name = u'Получателя рассылки'
        verbose_name_plural = u'Получатели рассылки'


    def __str__(self):
        return self.useremail
