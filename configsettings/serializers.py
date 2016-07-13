from rest_framework import serializers
from level.models import Level
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


    type                  = serializers.CharField(max_length=10)
    threshold             = serializers.CharField(max_length=10)
    rate                  = serializers.IntegerField()
    check_rate            = serializers.IntegerField()
    limit           = serializers.IntegerField()
    remit_discount        = serializers.PrimaryKeyRelatedField(required=False,
                                                                queryset=Level.objects.all())
    online_discount        = serializers.PrimaryKeyRelatedField(required=False,
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
