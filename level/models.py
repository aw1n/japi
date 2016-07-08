from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import timedelta

# Create your models here.
class WithdrawFeeWayField(object):
    ''' 
    @class WithdrawFeeWayField
    @brief
        Implements WithdrawFeeWay type of field.
        Withdraw_fee_way is of type integer with the ff. possible values:
        0 - for free
        1 - for always
        2 - according to settings
    '''

    def __init__(self, max_length='10'):
        '''
        @fn __init__
        '''

        self.max_length = max_length
        # if len(self.name) > self.max_length:
        #     print('Withdraw fee way must be upto {0} digits'.format(max_length))


class Level(models.Model):
    '''
    @class Level
    @brief
        Level model class
    '''

    # Level model fields
    id                    = models.AutoField(primary_key=True)
    name                  = models.CharField(max_length=255)
    com_remit_limit       = models.CommaSeparatedIntegerField(max_length=255)
    com_remit_derate      = models.CommaSeparatedIntegerField(max_length=10)
    online_pay_limit      = models.CommaSeparatedIntegerField(max_length=255)
    online_pay_derate     = models.CommaSeparatedIntegerField(max_length=10)
    withdraw_limit        = models.CommaSeparatedIntegerField(max_length=255)
    withdraw_fee          = models.FloatField() #TODO: add validators? max_length = 255
    withdraw_fee_way      = models.IntegerField()
    withdraw_fee_settings = WithdrawFeeWayField(max_length=10) #TODO: add arguments? 
    reg_present           = models.CommaSeparatedIntegerField(max_length=10)
    remit_check_rate      = models.CommaSeparatedIntegerField(max_length=10)
    service_rate          = models.IntegerField()
    memo                  = models.TextField()
    status                = models.IntegerField()
    cdt_deposit_num       = models.IntegerField()
    cdt_deposit_amount    = models.IntegerField()
    cdt_deposit_max       = models.IntegerField()
    cdt_withdraw_num      = models.IntegerField()
    cdt_withdraw_amount   = models.IntegerField()

    def __str__(self):
        return self.name