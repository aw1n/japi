import datetime
from rest_framework import serializers
from django.db import IntegrityError
from bank.models import Bank

class BankSerializer(serializers.ModelSerializer):
    '''
    @class AgentSerializer
    @brief
        Serializer for Agent
    '''

    # def __init__(self, *args, **kwargs):
    #     '''
    #     '''

    #     super(BankSerializer, self).__init__(*args, **kwargs)
    #     opt_fields = self.context['request'].query_params.get('opt_fields')
    #     if opt_fields:
    #         opt_fields = opt_fields.split(',')
    #         # Remove not specified fields
    #         to_show = set(opt_fields)
    #         default = set(self.fields.keys())
    #         for field in default - to_show:
    #             self.fields.pop(field)

    class Meta:
        model = Bank
        fields = ('id', 'bank_name', 'province', 'city', 'account', 'memo')
        # extra_kwargs = {'id':{'read_only': False, 'required': False}}