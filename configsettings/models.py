from __future__ import unicode_literals

from django.db import models
from level.models import Level
from provider.models import Provider
from gametype.models import GameType

STATUS_OPTIONS = (
    (0, 'Inactive'),
    (1, 'Active')
)


class ReturnSettings(models.Model):
    '''
    @class ReturnSettings
    @brief
        ReturnSettings model class
    '''

    name = models.CharField(max_length=255)
    status = models.IntegerField(default=0, choices=STATUS_OPTIONS)

    class Meta:
        db_table = "configsettings_returnsettings"

    def __unicode__(self):
        return self.name


class ReturnGroup(models.Model):
    '''
    @class ReturnRateConfig
    @brief
        ReturnRateConfig model class
    '''

    threshold = models.IntegerField(default=0)
    max = models.IntegerField(null=True, blank=True)
    check_amount = models.IntegerField(null=True, blank=True)
    return_setting = models.ForeignKey(ReturnSettings, null=True, related_name='returngroup_settings')

    class Meta:
        db_table = 'configsettings_returngroup'


class ReturnRate(models.Model):
    '''
    @class ReturnRate
    @brief
        ReturnRate model class
    '''

    provider = models.ForeignKey(Provider, related_name='provider_returnconfig')
    type = models.ForeignKey(GameType, related_name='type_returnconfig')
    rate = models.FloatField()
    return_config = models.ForeignKey(ReturnGroup, null=True, related_name='returnconfig_group')

    class Meta:
        db_table = 'configsettings_returnrate'


class CommissionSettings(models.Model):

    name = models.CharField(max_length=100)
    status = models.IntegerField(default=0, choices=STATUS_OPTIONS)
    invest_least = models.IntegerField() #minimum bet
    deposit_fee = models.IntegerField() #single deposit fee
    deposit_fee_max = models.IntegerField() #deposit fee cap
    withdraw_fee = models.IntegerField() #single withdrawal fees
    withdraw_fee_max = models.IntegerField() #withdrawal fee cap

    class Meta:
        db_table = 'configsettings_commissionsettings'


class CommissionGroup(models.Model):
    '''
    @class CommissionGroup
    @brief
        CommissionGroup model class
    '''

    threshold = models.IntegerField(default=0)
    member_num = models.IntegerField()
    discount_rate = models.FloatField()
    return_rate = models.FloatField()
    commission_setting = models.ForeignKey(CommissionSettings, null=True, related_name='commgroup_settings')

    class Meta:
        db_table = 'configsettings_commissiongroup'


class CommissionRate(models.Model):
    '''
    @class CommissionRate
    @brief
        CommissionRate model class
    '''

    provider = models.ForeignKey(Provider, related_name='provider_commissionconfig')
    type = models.ForeignKey(GameType, related_name='type_commissionconfig')
    rate = models.FloatField()
    commission_group = models.ForeignKey(CommissionGroup,
                                        related_name='commissionrate_group',
                                        null=True)

    class Meta:
        db_table = 'configsettings_commissionrate'


class Discount(models.Model):
    '''
    @class Discount
    @brief
        Discount model class
    '''

    type = models.CharField(max_length=10)
    threshold = models.CommaSeparatedIntegerField(max_length=10)
    rate = models.FloatField()
    check_rate = models.FloatField()
    limit = models.CharField(max_length=50, blank=True, null=True)
    # many-to-one with Level
    remit_discount = models.ForeignKey(Level, related_name='level_remit_discount', blank=True, null=True)
    online_discount = models.ForeignKey(Level, related_name='level_online_discount', blank=True, null=True)

    class Meta:
        db_table = "configsettings_discount"

