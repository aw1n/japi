from rest_framework import serializers, renderers, parsers
from level.models import Level
from configsettings.models import Discount
from configsettings.serializers import DiscountSerializer

import json
import ast


class LevelSerializer(serializers.ModelSerializer):
    '''
    @class LevelSerializer
    @brief
        Serializer class for Level
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(LevelSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            opt_fields = self.context['request'].query_params.get('opt_fields')
            if opt_fields:
                opt_fields = opt_fields.split(',')
                # Remove not specified fields
                to_show = set(opt_fields)
                default = set(self.fields.keys())
                for field in default - to_show:
                    self.fields.pop(field)

    member_count = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    remit_limit  = serializers.CharField(required=False, max_length=255, allow_null=True)
    online_limit = serializers.CharField(required=False, max_length=255, allow_null=True)
    withdraw_limit = serializers.CharField(required=False, max_length=255, allow_null=True)
    # withdraw_fee = serializers.FloatField()
    withdraw_fee = serializers.CharField(max_length=100)
    reg_present = serializers.CharField(required=False, max_length=100, allow_null=True)
    remit_check = serializers.CharField(max_length=100, allow_null=True)
    service_rate = serializers.IntegerField()
    memo = serializers.CharField(required=False)
    status = serializers.IntegerField(default=1, allow_null=True)
    cdt_deposit_num = serializers.IntegerField(required=False, allow_null=True)
    cdt_deposit_amount = serializers.IntegerField(required=False, allow_null=True)
    cdt_deposit_max = serializers.IntegerField(required=False, allow_null=True)
    cdt_withdraw_num = serializers.IntegerField(required=False, allow_null=True)
    cdt_withdraw_amount = serializers.IntegerField(required=False, allow_null=True)
    remit_discounts = DiscountSerializer(required=False, source='level_remit_discount', many=True)
    online_discounts = DiscountSerializer(required=False, source='level_online_discount', many=True)
    __fields_to_validate = [
                            'remit_limit',
                            'online_limit',
                            'withdraw_limit',
                            'withdraw_fee',
                            'reg_present',
                            'remit_check',
                            ]
    

    class Meta:
        model = Level
        depth = 2
        fields = (
                'member_count',
                'id',
                'name',
                'remit_limit',
                'online_limit',
                'withdraw_limit',
                'withdraw_fee',
                # 'withdraw_fee_way',
                'reg_present',
                'remit_check',
                'service_rate',
                'memo',
                'status',
                'cdt_deposit_num',
                'cdt_deposit_amount',
                'cdt_deposit_max',
                'cdt_withdraw_num',
                'cdt_withdraw_amount',
                'remit_discounts',
                'online_discounts',)

    def validate(self, data):
        '''
        @fn validate
        @brief
            Validates the data of the serializer.
            Specified field names needs to be a string convertible
            to python dictionary in order to be valid.
        '''

        validated_data = dict()
        try:
            for key, value in data.iteritems():
                if key in self.__fields_to_validate:
                    # check if can be converted to dictionary
                    if ast.literal_eval(value):
                        pass # value is a valid string dictionary
                validated_data[key] = value
        except:
            raise serializers.ValidationError('Invalid data')

        return validated_data
