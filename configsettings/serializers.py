from rest_framework import serializers
from level.models import Level
from configsettings.models import Discount, ReturnSettings, ReturnRateConfig
from gametype.models import GameType
from gametype.serializers import GameTypeSerializer
from provider.models import Provider
from provider.serializers import ProviderSerializer
from configsettings.models import Discount, CommissionSettings


class DiscountSerializer(serializers.ModelSerializer):
    '''
    @class DiscountSerializer
    @brief
        Serializer class for Discount
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(DiscountSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            opt_fields = self.context['request'].query_params.get('opt_fields')
            if opt_fields:
                opt_fields = opt_fields.split(',')
                # Remove not specified fields
                to_show = set(opt_fields)
                default = set(self.fields.keys())
                for field in default - to_show:
                    self.fields.pop(field)


    type = serializers.CharField(max_length=10)
    threshold = serializers.CharField(max_length=10)
    rate = serializers.FloatField()
    check_rate = serializers.IntegerField()
    limit = serializers.IntegerField()
    remit_discount = serializers.PrimaryKeyRelatedField(required=False,
                                                        queryset=Level.objects.all())
    online_discount = serializers.PrimaryKeyRelatedField(required=False,
                                                        queryset=Level.objects.all())

    class Meta:
        model = Discount
        fields = (
                'type',
                'threshold',
                'rate',
                'check_rate',
                'limit',
                'remit_discount',
                'online_discount')


class ReturnRateConfigSerializer(serializers.ModelSerializer):
    '''
    @class ReturnRateConfigSerializer
    @brief
        Serializer class for ReturnRateConfigSerializer
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(ReturnRateConfigSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            opt_fields = self.context['request'].query_params.get('opt_fields')
            if opt_fields:
                opt_fields = opt_fields.split(',')
                # Remove not specified fields
                to_show = set(opt_fields)
                default = set(self.fields.keys())
                for field in default - to_show:
                    self.fields.pop(field)

    provider = serializers.PrimaryKeyRelatedField(required=False,
                                                    queryset=Provider.objects.all())
    type = serializers.PrimaryKeyRelatedField(required=False,
                                                queryset=GameType.objects.all())
    rate = serializers.FloatField()
    threshold = serializers.IntegerField(default=0)
    max = serializers.IntegerField(required=False, allow_null=True)
    check_amount = serializers.IntegerField(required=False, allow_null=True)
    return_setting = serializers.PrimaryKeyRelatedField(required=False,
                                                        allow_null=True,
                                                        queryset=ReturnSettings.objects.all()) 


    class Meta:
        model = ReturnRateConfig
        fields = (
                'provider',
                'type',
                'rate',
                'threshold',
                'max',
                'check_amount',
                'return_setting'
                )


class ReturnSettingsSerializer(serializers.ModelSerializer):
    '''
    @class ReturnSettingsSerializer
    @brief
        Serializer class for ReturnSettingsSerializer
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(ReturnSettingsSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            opt_fields = self.context['request'].query_params.get('opt_fields')
            if opt_fields:
                opt_fields = opt_fields.split(',')
                # Remove not specified fields
                to_show = set(opt_fields)
                default = set(self.fields.keys())
                for field in default - to_show:
                    self.fields.pop(field)

    name = serializers.CharField(max_length=255)
    config = ReturnRateConfigSerializer(required=False, source='returnrate_settings', many=True)


    class Meta:
        model = ReturnSettings
        fields = ('name', 'status', 'config')

    def validate(self, data):
        '''
        '''


        returnrateconfigs = self.context.get('returnrateconfigs')
        print(data)
        return data


class RateConfigRetrieveSerializer(serializers.ModelSerializer):
    '''
    @class RateConfigRetrieveSerializer
    @brief
        Serializer class for RateConfigRetrieveSerializer
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(RateConfigRetrieveSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            opt_fields = self.context['request'].query_params.get('opt_fields')
            if opt_fields:
                opt_fields = opt_fields.split(',')
                # Remove not specified fields
                to_show = set(opt_fields)
                default = set(self.fields.keys())
                for field in default - to_show:
                    self.fields.pop(field)

    provider = ProviderSerializer()
    type = GameTypeSerializer()
    return_setting = ReturnSettingsSerializer()

    class Meta:
        model = ReturnRateConfig
        fields = (
                'provider',
                'type',
                'rate',
                'threshold',
                'max',
                'check_amount',
                'return_setting'
                )


class CommissionSettingsSerializer(serializers.ModelSerializer):
    '''
    @class CommissionSettingsSerializer
    @brief
        Serializer for Commission Settings
    '''

    class Meta:
        model = CommissionSettings
        fields = ('name', 
                    'status', 
                    'invest_least',   
                    'deposit_fee',     
                    'deposit_fee_max', 
                    'withdraw_fee',    
                    'withdraw_fee_max')
