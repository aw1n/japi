from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import timedelta

LEVEL_STATUS_OPTIONS = (
                        (1, 'NORMAL'),
                        (0, 'DANGEROUS'),
                        )


class Level(models.Model):
    '''
    @class Level
    @brief
        Level model class
    '''

    # Level model fields
    name = models.CharField(max_length=255)
    remit_limit = models.CharField(max_length=255, blank=True, null=True)
    online_limit = models.CharField(max_length=255, blank=True, null=True)
    withdraw_limit = models.CharField(max_length=255, blank=True, null=True)
    # withdraw_fee = models.FloatField()
    withdraw_fee = models.CharField(max_length=100, blank=True, null=True)
    # withdraw_fee_settings = models.CharField(max_length=50, blank=True, null=True)
    reg_present = models.CharField(max_length=100, blank=True, null=True)
    remit_check = models.CharField(max_length=100, blank=True, null=True)
    service_rate = models.IntegerField()
    memo = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=1, choices=LEVEL_STATUS_OPTIONS)
    cdt_deposit_num = models.IntegerField(blank=True, null=True)
    cdt_deposit_amount = models.IntegerField(blank=True, null=True)
    cdt_deposit_max = models.IntegerField(blank=True, null=True)
    cdt_withdraw_num = models.IntegerField(blank=True, null=True)
    cdt_withdraw_amount = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = "level_level"

    def __unicode__(self):
        return self.name