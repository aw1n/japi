import datetime
from rest_framework import serializers
from django.db import IntegrityError
from bank.models import Bank

class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = ('id', 'bank_name', 'province', 'city', 'account', 'memo')
        extra_kwargs = {'id':{'read_only': False, 'required': False}}