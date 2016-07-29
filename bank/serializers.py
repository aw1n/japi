import datetime
from rest_framework import serializers
from django.db import IntegrityError
from bank.models import Bank, BankInfo

class BankInfoSerializer(serializers.ModelSerializer):
    '''
    @class BankInfoSerializer
    @brief
        Serializer for BankInfo
    '''
    class Meta:
        model = BankInfo
        fields = ('id', 'bank', 'province', 'city', 'account', 'memo')
        extra_kwargs = {'id':{'read_only': False, 'required': False},
                        'bank':{'read_only': False, 'required': False}}

class BankSerializer(serializers.ModelSerializer):
    '''
    @class BankSerializer
    @brief
        Serializer for Bank
    '''
    class Meta:
        model = Bank
        fields = ('id', 'name', 'rank')
