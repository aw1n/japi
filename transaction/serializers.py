import uuid
import hashlib
import datetime
from rest_framework import serializers
from django.contrib.auth.models import User

from account.models import Member
from level.models import Level
from .models import RemitInfo, RemitPayee, Transaction, TransactionType, PaymentType, OnlinePayee
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