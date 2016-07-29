from __future__ import unicode_literals

from django.db import models

STATUS_OPTIONS = (
    (0, 'Inactive'),
    (1, 'Active')
)


class Provider(models.Model):
    '''
    @class Provider
    @brief
        Provider model class
    '''

    name = models.CharField(max_length=255)
    status = models.IntegerField(default=1, choices=STATUS_OPTIONS)


    class Meta:
        db_table = 'provider_provider'

    def __unicode__(self):
        return self.name
