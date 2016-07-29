from rest_framework import serializers
from level.models import Level
from configsettings.models import (
                                    Discount,
                                    ReturnSettings,
                                    ReturnGroup,
                                    ReturnRate,
                                    CommissionSettings,
                                    CommissionRate,
                                    CommissionGroup
                                    )
from jaguar.lib.optionfieldsfilter import OptionFieldsFilter
from gametype.models import GameType
from gametype.serializers import GameTypeSerializer
from provider.models import Provider
from provider.serializers import ProviderSerializer
from rest_framework.parsers import JSONParser


class DiscountSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class DiscountSerializer
    @brief
        Serializer class for Discount
    '''

    type = serializers.CharField(max_length=10)
    threshold = serializers.CharField(max_length=10)
    rate = serializers.FloatField()
    check_rate = serializers.FloatField()
    limit = serializers.CharField(allow_null=True)
    # remit_discount = serializers.PrimaryKeyRelatedField(required=False,
    #                                                     queryset=Level.objects.all())
    # online_discount = serializers.PrimaryKeyRelatedField(required=False,
    #                                                     queryset=Level.objects.all())

    class Meta:
        model = Discount
        fields = (
                'id',
                'type',
                'threshold',
                'rate',
                'check_rate',
                'limit')


class ReturnGroupSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class ReturnGroupSerializer
    @brief
        Serializer class for ReturnGroupSerializer
    '''

    threshold = serializers.IntegerField(default=0)
    max = serializers.IntegerField(required=False, allow_null=True)
    check_amount = serializers.IntegerField(required=False, allow_null=True)
    return_setting = serializers.PrimaryKeyRelatedField(required=False,
                                                        allow_null=True,
                                                        queryset=ReturnSettings.objects.all())

    class Meta:
        model = ReturnGroup
        fields = (
                'threshold',
                'max',
                'check_amount',
                'return_setting'
                )

class ReturnRateSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class ReturnRateSerializer
    @brief
        Serializer class for ReturnRateSerializer
    '''

    provider = ProviderSerializer()
    type = GameTypeSerializer()

    class Meta:
        model = ReturnRate
        fields = (
                'id',
                'provider',
                'type',
                'rate'
                )


class ReturnGroupForSettingsSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class RateConfigForSettingsSerializer
    @brief
        Serializer class for ReturnRateConfigSerializer
    '''

    # provider = ProviderSerializer()
    rates = ReturnRateSerializer(required=False, source='returnconfig_group', many=True)
    threshold = serializers.IntegerField(default=0)
    max = serializers.IntegerField(required=False, allow_null=True)
    check_amount = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = ReturnGroup
        fields = (
                'id',
                'rates',
                'threshold',
                'max',
                'check_amount',
                )

class ReturnSettingsSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class ReturnSettingsSerializer
    @brief
        Serializer class for ReturnSettings
    '''

    name = serializers.CharField(max_length=255)
    groups = ReturnGroupForSettingsSerializer(required=False, source='returngroup_settings', many=True)

    class Meta:
        model = ReturnSettings
        fields = ('id', 'name', 'status', 'groups')


class ReturnSettingsForConfigSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class ReturnSettingsForConfigSerializer
    @brief
        Serializer class for ReturnSettings
    '''

    name = serializers.CharField(max_length=255)

    class Meta:
        model = ReturnSettings
        fields = ('name', 'status')


class RateConfigRetrieveSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class RateConfigRetrieveSerializer
    @brief
        Serializer class for RateConfigRetrieveSerializer
    '''

    provider = ProviderSerializer()
    type = GameTypeSerializer()
    return_setting = ReturnSettingsForConfigSerializer(required=False)

    class Meta:
        model = ReturnGroup
        fields = (
                'provider',
                'type',
                'rate',
                'threshold',
                'max',
                'check_amount',
                'return_setting',
                )


class CommissionRateSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class CommissionRateSerializer
    @brief
        Serializer class for CommissionRate
    '''

    provider = ProviderSerializer()
    type = GameTypeSerializer()

    class Meta:
        model = CommissionRate
        fields = ('provider', 'type', 'rate')


class CommissionGroupForSettingsSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    '''

    rates = CommissionRateSerializer(required=False, source='commissionrate_group', many=True)

    class Meta:
        model = CommissionGroup
        fields = ('id',
                    'threshold',
                    'member_num',
                    'discount_rate',
                    'return_rate',
                    'rates')


class CommissionSettingsSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class CommissionSettingsSerializer
    @brief
        Serializer for Commission Settings
    '''

    groups = CommissionGroupForSettingsSerializer(required=False,
                                                    source='commgroup_settings',
                                                    many=True)

    class Meta:
        model = CommissionSettings
        fields = (
                'id',
                'name',
                'status',
                'invest_least',
                'deposit_fee',
                'deposit_fee_max',
                'withdraw_fee',
                'withdraw_fee_max',
                'groups'
                )


class CommissionSettingsForListSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class CommissionSettingsForListSerializer
    @brief
        Serializer for Commission Settings
    '''

    group_count = serializers.IntegerField(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    agent_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CommissionSettings
        fields = (
                'id',
                'name',
                'status',
                'invest_least',
                'group_count',
                'member_count',
                'agent_count',
                'deposit_fee',
                'deposit_fee_max',
                'withdraw_fee',
                'withdraw_fee_max'
                )


class ReturnSettingsForListSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class ReturnSettingsForListSerializer
    @brief
        Serializer class for ReturnSettings
    '''

    group_count = serializers.IntegerField(read_only=True)
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ReturnSettings
        fields = (
                'id',
                'name',
                'status',
                'group_count',
                'member_count'
                )
