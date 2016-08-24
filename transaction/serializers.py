import uuid
import hashlib
import datetime
import ast
from rest_framework import serializers
from django.contrib.auth.models import User

from account.models import Member
from level.models import Level
from .models import RemitInfo, RemitPayee, Transaction, TransactionType, PaymentType, OnlinePayee, Balance
from jaguar.lib.validators import RequiredFieldValidator
from jaguar.lib.paymentgateway import PaymentGateway


class RemitInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RemitInfo
        fields = ('id', 'bank', 'way', 'depositor', 'deposited_at', 'created_at', 'transaction_remit_info')
        depth = 1

    def to_internal_value(self, data):
        RequiredFieldValidator.validate(data, ('remit_info',))

        #validate
        member = data.get('member')
        data['member'] = Member.objects.get(pk=member) if member else None

        transaction_type = data.get('transaction_type')
        data['transaction_type'] = TransactionType.objects.get(pk=transaction_type) if transaction_type else None

        return data

    def create(self, data):
        remit_info_data = data.pop('remit_info', None)
        remit_info = RemitInfo.objects.create(**remit_info_data) if remit_info_data else None
        if remit_info:
            transaction = Transaction.objects.create(remit_info=remit_info, **data)
        return remit_info


class RemitPayeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemitPayee


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType


class OnlinePayeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlinePayee
        depth = 2

    def to_internal_value(self, data):
        return data

    def create(self, data):
        member_levels = data.pop('member_levels', None)
        payment_type = data.get('payment_type')
        data['payment_type'] = PaymentType.objects.get(pk=payment_type) if payment_type else None
        online_payee = OnlinePayee.objects.create(**data)

        if member_levels:
            for level_id in member_levels:
                level = Level.objects.get(pk=level_id)
                online_payee.level.add(level)
        return online_payee

    def to_representation(self, obj):
        ret = super(OnlinePayeeSerializer, self).to_representation(obj)

        payment_type = ret.get('payment_type')
        if payment_type:
            ret['payment_type'] = {'id': payment_type['id'], 'name': payment_type['name']}

        level = ret.get('level')
        if level:
            member_levels = []
            for x in level:
                member_levels.append({'id': x['id'], 'name': x['name']})
            ret['level'] = member_levels
        return ret


class TransactionSerializer(serializers.ModelSerializer):
    remit_info = RemitInfoSerializer(required=False)
    online_payee = OnlinePayeeSerializer(required=False)

    class Meta:
        model = Transaction

    def create(self, validated_data):
        remit_info_data = validated_data.pop('remit_info', None)
        remit_info = RemitInfo.objects.create(**remit_info_data) if remit_info_data else None
        if remit_info:
            validated_data['remit_info'] = remit_info

        transaction = Transaction.objects.create(**validated_data)

        return transaction


class OnlinePaymentSerializer(TransactionSerializer):
    class Meta:
        model = Transaction

    def generate_transaction_id(self):
        unique_id = str(uuid.uuid4().fields[0])
        datetime_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return '{}{}'.format(datetime_now,unique_id)

    def create(self, data):
        transaction = Transaction.objects.create(**data)
        return transaction

    def validate(self, data):
        request = self.context['request']
        online_payee = OnlinePayee.objects.get(pk=request.data.get('merchant_num')) if request.data.get('merchant_num') else None
        member = Member.objects.get(pk=request.data.get('member_id')) if request.data.get('member_id') else None

        if request.method == 'POST':
            RequiredFieldValidator.validate(data, ('amount',))
            data['status'] = 3
            data['member_id'] = member.id if member else None
            data['transaction_id'] = self.generate_transaction_id()
            data['online_payee_id'] = online_payee.id
            data['transaction_type'] = TransactionType.objects.get(code='online_pay')
        return data

    def to_representation(self, obj):
        request = self.context['request']

        merchant_num = request.data.get('merchant_num')
        if merchant_num:
            return PaymentGateway.generate_data(merchant_num, obj)

        else:
            raise NotFound('Merchant number not found.')


class WithdrawTransactionSerializer(TransactionSerializer):
    '''
    '''

    class Meta:
        model = Transaction

    def generate_transaction_id(self):
        '''
        '''

        unique_id = str(uuid.uuid4().fields[0])
        datetime_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return '{}{}'.format(datetime_now,unique_id)

    def create(self, data):
        '''
        '''

        transaction = Transaction.objects.create(**data)
        return transaction

    def validate(self, data):
        '''
        '''

        request = self.context['request']
        RequiredFieldValidator.validate(data, ('amount',))

        if not request.data.get('member_id'):
            raise serializers.ValidationError('Member id is required')
        if not request.data.get('withdraw_password'):
            raise serializers.ValidationError('Withdraw password is required')

        try:
            member = Member.objects.get(pk=request.data.get('member_id'))
            amount = float(data['amount'])
        except DoesNotExist:
            raise serializers.ValidationError('Member not found!')
        except ValueError:
            raise serializers.ValidationError('Invalid amount...')

        if request.data.get('withdraw_password') != member.withdraw_password:
            raise serializers.ValidationError('Password is incorrect!')

        member_lv = member.level
        withdraw_limit = ast.literal_eval(member_lv.withdraw_limit)
        withdraw_fee_dict = ast.literal_eval(member_lv.withdraw_fee)

        withdraw_fee = 0
        if withdraw_fee_dict.get('value'):
            withdraw_fee = float(withdraw_fee_dict.get('value'))
        balance = member.balance_member.all()[0].balance

        if not amount + withdraw_fee <= balance:
            raise serializers.ValidationError('Insufficient balance...')

        upper_withdraw_limit = balance
        lower_withdraw_limit = 0
        if withdraw_limit.get('upper'):
            upper_withdraw_limit = float(withdraw_limit.get('upper'))
        if withdraw_limit.get('lower'):
            lower_withdraw_limit = float(withdraw_limit.get('lower'))

        if amount >= lower_withdraw_limit and amount <= upper_withdraw_limit:
            data['amount'] = amount
            data['status'] = 3
            data['member_id'] = member.id
            data['transaction_id'] = self.generate_transaction_id()
            data['transaction_type'] = TransactionType.objects.get(code='withdraw')
        else:
            raise serializers.ValidationError('Invalid amount...')
        return data


class BalanceTransactionSerializer(serializers.ModelSerializer):
    '''
    '''

    class Meta:
        model = Balance


    def validate(self, data):
        '''
        '''

        request = self.context['request']
        try:
            transaction = Transaction.objects.get(transaction_id=request.data.get('transaction_id'))
        except DoesNotExist:
            raise serializers.ValidationError('Transaction not found!')
        data['amount'] = transaction.amount
        data['transaction'] = transaction
        if transaction.transaction_type == TransactionType.objects.get(code='withdraw'):
            member = transaction.member
            member_lv = member.level
            withdraw_fee_dict = ast.literal_eval(member_lv.withdraw_fee)
            withdraw_fee = 0
            if withdraw_fee_dict.get('value'):
                withdraw_fee = float(withdraw_fee_dict.get('value'))
            data['withdraw_fee'] = withdraw_fee
            data['transaction_type'] = 'withdraw'

        return data

    def create(self, validated_data):
        member = validated_data.get('transaction').member
        balance_inst = Balance.objects.get(member=member.pk)
        if validated_data['transaction_type'] == 'withdraw':
            balance = balance_inst.balance
            balance -= validated_data['amount'] + validated_data['withdraw_fee']
            setattr(balance_inst, 'balance', balance)
        balance_inst.save()
        return balance_inst
