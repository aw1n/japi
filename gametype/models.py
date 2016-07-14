from __future__ import unicode_literals

from django.db import models
from provider.models import Provider

STATUS_OPTIONS = (
    ('0', 'Inactive'),
    ('1', 'Active')
)


class GameType(models.Model):
    '''
    '''

    name = models.CharField(max_length=255)
    status = models.IntegerField(default=1, choices=STATUS_OPTIONS)
    provider = models.ForeignKey(Provider, related_name='game_provider')


    def __str__(self):
        '''
        '''

        return self.name

    class Meta:
        db_table = 'gametype_gametype'
