from rest_framework import serializers

from account.models import Member
from .models import RemitInfo, Transaction, TransactionType, PaymentType, OnlinePayee
from jaguar.lib.validators import RequiredFieldValidator


class RemitInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemitInfo
        fields = ('id', 'bank', 'way', 'depositor', 'deposited_at', 'created_at')


class OnlinePayeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlinePayee


class TransactionSerializer(serializers.ModelSerializer):
    remit_info = RemitInfoSerializer(required=False)

    class Meta:
        model = Transaction

    def create(self, validated_data):
        remit_info_data = validated_data.pop('remit_info', None)
        remit_info = RemitInfo.objects.create(**remit_info_data)

        if remit_info:
            transaction = Transaction.objects.create(remit_info=remit_info, **validated_data)

        return transaction


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
