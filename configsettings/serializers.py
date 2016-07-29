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
    limit = serializers.CharField(allow_null=True, required=False)
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

    def to_internal_value(self, data):
        pass

    def validate(self, data):
        '''
        '''

        request = self.context['request']

        if request.method == 'POST' or request.method == 'PUT':
            data = request.data

        return data

    def create(self, validated_data):
        # get groups details
        returngroups = validated_data.get('groups', None)
        validated_data.pop('groups', None)

        returnsetting = ReturnSettings(**validated_data)
        returnsetting.save()
        # create/update return groups
        self.__update_return_groups(returnsetting, returngroups)
        return returnsetting

    def update(self, instance, validated_data):
        # get groups details
        returngroups = validated_data.get('groups', None)
        validated_data.pop('groups', None)

        # update instance details
        for key, val in validated_data.iteritems():
            setattr(instance, key, val)
        instance.save()

        # create/update return groups
        self.__update_return_groups(instance, returngroups)
        return instance

    def __update_return_groups(self, instance, returngroups):
        '''
        '''

        if returngroups is not None:
            instance.returngroup_settings.clear()
            for group in returngroups:
                group_dict = {
                    'threshold' : group['threshold'],
                    'max' : group['max'],
                    'check_amount' : group['check_amount']
                }

                if group.get('id'):
                    group_obj = ReturnGroup.objects.get(pk=group['id'])
                    group_obj.returnconfig_group.clear()
                    for item, val in group_dict.iteritems():
                        setattr(group_obj, item, val)
                    group_obj.save()
                    instance.returngroup_settings.add(group_obj)
                else:
                    group_obj = instance.returngroup_settings.create(**group_dict)

                # create/update rate
                rates = group['rates']
                for rate in rates:

                    rate_cpy = rate.copy()
                    rate_cpy.pop('name', None)
                    rate_cpy.pop('status', None)

                    provider_inst = Provider.objects.get(id=rate.get('provider'))
                    rate_cpy['provider'] = provider_inst

                    if not provider_inst:
                        response['error'] = 'Provider not found'
                        break

                    for gametype in rate.get('gametypes'):
                        gametype_inst = GameType.objects.get(id=gametype.get('type'))

                        if not gametype_inst:
                            response['error'] = 'Gametype not found'
                            break

                        gametype.pop('name')
                        gametype.pop('status')
                        rate_cpy.update(gametype)

                        if 'gametypes' in rate_cpy:
                            rate_cpy.pop('gametypes')
                        rate_cpy['type'] = gametype_inst
                        if 'id' not in gametype:
                            # create returnrate
                            # if returnrate with same data already exists delete it
                            __existing_rate = ReturnRate.objects.filter(**rate_cpy)
                            if __existing_rate:
                                __existing_rate.delete()
                            returnrate = group_obj.returnconfig_group.create(**rate_cpy)
                            continue

                        # update returnrate
                        rate_to_update = ReturnRate.objects.get(pk=rate.get('id'))

                        for key, value in rate_cpy.iteritems():
                            setattr(rate_to_update, key, value)
                        rate_to_update.save()
        return


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

    def to_internal_value(self, data):
        pass

    def validate(self, data):
        '''
        '''

        request = self.context['request']

        if request.method == 'POST' or request.method == 'PUT':
            data = request.data

        return data

    def create(self, validated_data):
        # get groups details
        commissiongroups = validated_data.get('groups', None)
        validated_data.pop('groups', None)

        commissionsetting = CommissionSettings(**validated_data)
        commissionsetting.save()
        # create/update return groups
        self.__update_return_groups(commissionsetting, commissiongroups)
        return commissionsetting

    def update(self, instance, validated_data):
        # get groups details
        commissiongroups = validated_data.get('groups', None)
        validated_data.pop('groups', None)

        # update instance details
        for key, val in validated_data.iteritems():
            setattr(instance, key, val)
        instance.save()

        # create/update return groups
        self.__update_return_groups(instance, commissiongroups)
        return instance

    def __update_return_groups(self, instance, commissiongroups):
        '''
        '''

        # create or update the groups
        if commissiongroups is not None:
            # clear the relationship to the groups
            instance.commgroup_settings.clear()
            for group in commissiongroups:
                group_dict = {
                                'threshold': group.get('threshold'),
                                'member_num': group.get('member_num'),
                                'discount_rate': group.get('discount_rate'),
                                'return_rate': group.get('return_rate')
                                }
                if group.get('id'):
                    group_obj = CommissionGroup.objects.get(pk=group['id'])
                    group_obj.commissionrate_group.clear()
                    for key, val in group_dict.iteritems():
                        setattr(group_obj, key, val)
                    group_obj.save()
                    instance.commgroup_settings.add(group_obj)
                else:
                    group_obj = instance.commgroup_settings.create(**group_dict)

                # create/update rate
                rates = group.get('rates')
                if rates:
                    for rate in rates:
                        rate_cpy = rate.copy()
                        rate_cpy.pop('name', None)
                        rate_cpy.pop('status', None)

                        provider_inst = Provider.objects.get(id=rate.get('provider'))
                        rate_cpy['provider'] = provider_inst

                        if not provider_inst:
                            response['error'] = 'Provider not found'
                            break
                        for gametype in rate.get('gametypes'):
                            gametype_inst = GameType.objects.get(id=gametype.get('type'))

                            if not gametype_inst:
                                response['error'] = 'Gametype not found'
                                break

                            gametype.pop('name')
                            gametype.pop('status')
                            rate_cpy.update(gametype)

                            if 'gametypes' in rate_cpy:
                                rate_cpy.pop('gametypes')
                            rate_cpy['type'] = gametype_inst
                            if 'id' not in gametype:
                                # create returnrate
                                # if commissionrate with same data already exists delete it
                                __existing_rate = CommissionRate.objects.filter(**rate_cpy)
                                if __existing_rate:
                                    __existing_rate.delete()
                                returnrate = group_obj.commissionrate_group.create(**rate_cpy)
                                continue

                            # update commissionrate
                            rate_to_update = CommissionRate.objects.get(pk=rate.get('id'))

                            for key, value in rate_cpy.iteritems():
                                setattr(rate_to_update, key, value)
                            rate_to_update.save()
        return


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
