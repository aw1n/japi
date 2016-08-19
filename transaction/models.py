from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from bank.models import Bank
from level.models import Level
from account.models import Member
from provider.models import Provider


DATA_PARSER_OPTIONS = (
    (1, 'XML'),
    (2, 'JSON')
)

REMIT_TYPE_OPTIONS = (
    (1, 'Normal'),
    (2, 'Wechat'),
    (3, 'Alipay')
)

PAYMENT_TYPE_OPTIONS = (
    (1, 'Normal'),
    (2, 'Card'),
    (3, 'Mobile')
)

TRANSACTION_STATUS_OPTIONS = (
    (1, 'Success'),
    (2, 'Failed'),
    (3, 'Ongoing'),
    (4, 'Cancelled')
)


class TransactionType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(unique=True, max_length=255, null=True, blank=True)


class PaymentType(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    payment_type = models.IntegerField(default=1, null=True, blank=True, choices=PAYMENT_TYPE_OPTIONS)
    function_name = models.CharField(max_length=255, null=True, blank=True)
    data_parser = models.IntegerField(default=1, null=True, blank=True, choices=DATA_PARSER_OPTIONS)


class RemitInfo(models.Model):
    bank = models.CharField(max_length=255, null=True, blank=True)
    way = models.CharField(max_length=255, null=True, blank=True)
    depositor = models.CharField(max_length=255, null=True, blank=True)
    deposited_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)


class RemitPayee(models.Model):
    remit_type = models.IntegerField(default=1, null=True, blank=True, choices=REMIT_TYPE_OPTIONS)
    payee_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    account = models.CharField(max_length=255, null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.ImageField(null=True, blank=True)
    sum_fund = models.FloatField(null=True, blank=True)
    bank = models.ForeignKey(Bank, null=True, blank=True, related_name='remit_payee_bank')
    level = models.ManyToManyField(Level, related_name='remit_payee_member_level')


class OnlinePayee(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, null=True, blank=True, related_name='online_payee_payment_type')
    board_url = models.CharField(max_length=255, null=False, blank=False)
    merchant_num = models.CharField(max_length=255, null=True, blank=True)
    certificate = models.CharField(max_length=255, null=True, blank=True)
    merchant_account = models.CharField(max_length=255, null=True, blank=True)
    expired_in = models.IntegerField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    sum_fund = models.FloatField(null=True, blank=True)
    level = models.ManyToManyField(Level, related_name='online_payee_member_level')


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(default=1, null=True, blank=True, choices=TRANSACTION_STATUS_OPTIONS)
    transaction_type = models.ForeignKey(TransactionType, null=True, blank=True, related_name='transaction_type')
    member = models.ForeignKey(Member, null=True, blank=True, related_name='transaction_member')
    remit_payee = models.ForeignKey(RemitPayee, null=True, blank=True, related_name='transaction_remit_payee')
    remit_info = models.ForeignKey(RemitInfo, null=True, blank=True, related_name='transaction_remit_info')
    online_payee = models.ForeignKey(OnlinePayee, null=True, blank=True, related_name='transaction_online_payee')
    amount = models.FloatField(null=True, blank=True)
    provider = models.ForeignKey(Provider, null=True, blank=True, related_name='transaction_provider')
    memo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(User,related_name="transaction_updated_by", null=True, blank=True)

    class Meta:
        db_table = 'transaction'


class Balance(models.Model):
    balance = models.FloatField(null=True, blank=True)
    member = models.ForeignKey(Member, null=True, blank=True, related_name='balance_member')
    withdraw_limit = models.FloatField(default=0, null=True, blank=True)
    bet_sum = models.FloatField(null=True, blank=True)