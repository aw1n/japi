from __future__ import unicode_literals

from django.db import models

class Bank(models.Model):
    '''
    @class Bank
    @brief
        Bank company infomations
    '''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    rank = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'bank_bank'
        

class BankInfo(models.Model):
    '''
    @class Bank
    @brief
        Bank infomations of members or agents
    '''

    id = models.AutoField(primary_key=True)
    bank  = models.ForeignKey(Bank, related_name="bankinfo")
    province = models.CharField(max_length=100)
    city  = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    memo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'bank_bankinfo'
