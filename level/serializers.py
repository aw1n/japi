from rest_framework import serializers, renderers, parsers
from level.models import Level
from configsettings.models import Discount
from configsettings.serializers import DiscountSerializer
from jaguar.lib.optionfieldsfilter import OptionFieldsFilter

import json
import ast
import collections

class SimpleLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = (
            'id',
            'name',
            )

class LevelSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class LevelSerializer
    @brief
        Serializer class for Level
    '''

    member_count = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    remit_limit = serializers.CharField(required=False, max_length=255, allow_null=True)
    online_limit = serializers.CharField(required=False, max_length=255, allow_null=True)
    withdraw_limit = serializers.CharField(required=False, max_length=255, allow_null=True)
    # withdraw_fee = serializers.FloatField()
    withdraw_fee = serializers.CharField(max_length=100)
    reg_present = serializers.CharField(required=False, max_length=100, allow_null=True)
    remit_check = serializers.CharField(max_length=100, allow_null=True)
    service_rate = serializers.IntegerField()
    memo = serializers.CharField(required=False, allow_blank=True)
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

    def to_internal_value(self, data):
        ret = super(LevelSerializer, self).to_internal_value(data)
        remit_discount = data.get('remit_discounts')
        online_discount = data.get('online_discounts')
        if remit_discount:
            ret['level_remit_discount'] = remit_discount
        if online_discount:
            ret['level_online_discount'] = online_discount
        return ret

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

    def create(self, validated_data):
        '''
        '''

        remit_discount = validated_data.get('level_remit_discount')
        online_discount = validated_data.get('level_online_discount')
        validated_data.pop('level_remit_discount', None)
        validated_data.pop('level_online_discount', None)

        level = Level(**validated_data)
        level.save()

        if remit_discount:
            self.__create_update_discount(level.level_remit_discount, remit_discount)
        if online_discount:
            self.__create_update_discount(level.level_online_discount, online_discount)

        level.save()
        return level

    def update(self, instance, validated_data):
        '''
        '''

        remit_discount = validated_data.get('level_remit_discount')
        online_discount = validated_data.get('level_online_discount')
        validated_data.pop('level_remit_discount', None)
        validated_data.pop('level_online_discount', None)

        for key, val in validated_data.iteritems():
            setattr(instance, key, val)
        instance.save()

        if remit_discount:
            self.__create_update_discount(instance.level_remit_discount, remit_discount)
        if online_discount:
            self.__create_update_discount(instance.level_online_discount, online_discount)

        instance.save()
        return instance

    def __create_update_discount(self, instance, discount_details={}):
        '''
        @fn __create_update_discount
        @brief
            Creates or updates discount details then adds the discount to the given level.
        '''

        # clear the relationship for the level discount instance
        instance.clear()

        # process new relationships

        for discount in discount_details:
            # check if every field exists
            vailded = [(key in discount and discount.get(key) != '' ) for key in ['rate', 'check_rate', 'threshold']]

            if False in vailded:
                continue

            # check if discout had id
            if not discount.get('id'):
                # create discount
                discount_inst = instance.create(**discount)
                discount_inst.save()
                continue

            # update existing discount
            to_update = Discount.objects.get(pk=discount.get('id'))

            for key, value in discount.iteritems():
                setattr(to_update, key, value)
            to_update.save()

            # add to level
            instance.add(to_update)
        return

    def to_representation(self, instance):
        '''
        '''

        request = self.context['request']
        ret = super(LevelSerializer, self).to_representation(instance)

        to_display = collections.OrderedDict()
        for key, val in ret.iteritems():
            if key in self.__fields_to_validate:
                val = collections.OrderedDict(ast.literal_eval(val))
            to_display[key] = val
        return to_display
