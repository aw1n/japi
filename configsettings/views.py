# -*- coding: utf-8 -*-
from rest_framework import renderers, viewsets, mixins, status, filters, parsers
from rest_framework.response import Response
from django.db.models import Count
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from configsettings.serializers import (DiscountSerializer,
                                        ReturnSettingsSerializer,
                                        CommissionSettingsSerializer,
                                        CommissionSettingsForListSerializer,
                                        ReturnSettingsForListSerializer)
from configsettings.models import (Discount,
                                    ReturnSettings,
                                    ReturnGroup,
                                    ReturnRate,
                                    CommissionSettings,
                                    CommissionRate,
                                    CommissionGroup)
from configsettings.filters import DiscountFilter, ReturnRateConfigFilter, ReturnSettingsFilter
from jaguar.utils import ESPagination
from provider.models import Provider
from gametype.models import GameType

import django_filters
import collections


class DiscountViewSet(mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    '''
    @class DiscountViewSet
    @brief
        View set for Discount model
        Handles HTTP requests such as GET, PUT, and POST
    '''

    queryset = Discount.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = DiscountSerializer
    filter_class = DiscountFilter
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('type')
    pagination_class = ESPagination


class ReturnSettingsViewSet(mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    '''
    @class ReturnSettingsViewSet
    @brief
        View set for ReturnSettings
        Handles HTTP requests such as POST, GET, PUT
    '''

    queryset = ReturnSettings.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = ReturnSettingsSerializer
    filter_class = ReturnSettingsFilter
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'status')
    pagination_class = ESPagination

    '''
    @brief data structure
        {
            id: 68,
            name: "ReturnSetting Name",
            status: 0,
            groups: [{
                threshold: 11,
                max: 11,
                check_amount: 11,
                id: 49, # return group ip
                rates: [{ # return rates
                    provider: 1, # rates are group by provider
                    name: "BBIN",
                    status: 1,
                    gametypes: [{
                        name: "Game type Name",
                        status: 1,
                        type: 1,
                        rate: 1
                    },{
                        name: "Game type Name",
                        status: 1,
                        type: 2,
                        rate: 1
                    }]
                },{
                    provider: 2,
                    name: "SABA",
                    status: 1,
                    gametypes: [{
                        name: "HTML5",
                        status: 1,
                        type: 3,
                        rate: 1
                    },{
                    name: "Game type Name",
                        status: 1,
                        type: 4,
                        rate: 1
                    }]
                }]
            }]
        }
    '''

    def list(self, request):
        '''
        '''

        response = dict()
        try:
            retunsettings = ReturnSettings.objects.annotate(group_count=Count('returngroup_settings'),
                                                            member_count=Count('member_return_settings'))

            # uncomment the next LOCs line if filter and pagination are supported.
            # retunsettings = self.filter_queryset(retunsettings)
            # retunsettings = self.paginate_query(retunsettings)

            serializer = ReturnSettingsForListSerializer(retunsettings,
                                                        context={'request': request},
                                                        many=True)

            return Response(serializer.data)
        except Exception as err:
            response['error']  = err
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data


        for group in data['groups']:
            # use new_rates to replace former rates field
            new_rates = []

            '''
            data structure for new_rate
                {
                    provider: 2,
                    name: "SABA",
                    status: 1,
                    gametypes: [{
                        name: "HTML5",
                        status: 1,
                        type: 3,
                        rate: 1
                    },{
                        name: "Game type Name",
                        status: 1,
                        type: 4,
                        rate: 1
                    }]
                }
            '''
            new_rate = dict()

            rates = group['rates']

            for rate in rates:
                provider = rate['provider']
                type_cpy = rate['type'].copy()
                type_cpy['rate'] = rate['rate']

                if ('provider' in new_rate and new_rate['provider'] == provider['provider']):
                    new_rate['gametypes'].append(type_cpy)
                else:
                    new_rate = rate['provider'].copy()
                    new_rate['gametypes'] = [type_cpy]
                    if new_rate:
                        new_rates.append(new_rate)

            # comment this line to see original data structure
            group['rates'] = new_rates

        return Response(serializer.data)

    def create(self, request):
        '''
        @fn create
        @brief
            Overrides create method (POST)
        '''

        return self.__update_create(request)

    def update(self, request, pk):
        '''
        @fn update
        @brief
            Overrides update method (PUT)
        '''

        return self.__update_create(request, pk)

    def __update_create(self, request, pk=None):
        response = dict()

        data = self.request.data

        returnsetting_dict = dict()
        if data.get('name'):
            returnsetting_dict['name'] = data.get('name')
        if data.get('status') or data.get('status') == 0:
            returnsetting_dict['status'] = data.get('status')

        returngroups = data.get('groups')
        if returngroups is not None:
            data.pop('groups')

        # build a ReturnSetting object first
        try:
            temp_dict = dict()
            if pk:
                returnsetting = ReturnSettings.objects.get(pk=pk)
                temp_dict = returnsetting.__dict__.copy()
                temp_dict.pop('_state')
                temp_dict.update(returnsetting_dict)
                returnsetting_dict = temp_dict
            else:
                returnsetting = ReturnSettings(**returnsetting_dict)

            serializer = ReturnSettingsSerializer(returnsetting,
                                                    data=returnsetting_dict,
                                                    context={'request': request})
            if not serializer.is_valid():
                response['error'] = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            # update return groups
            if returngroups is not None:
                returnsetting.returngroup_settings.clear()
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
                        returnsetting.returngroup_settings.add(group_obj)
                    else:
                        group_obj = returnsetting.returngroup_settings.create(**group_dict)

                    # create/update rate
                    rates = group['rates']
                    for rate in rates:

                        rate_cpy = rate.copy()
                        rate_cpy.pop('name')
                        rate_cpy.pop('status')

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

            if response:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            response['error'] = 'ReturnSettings with id={0} not found'.format(pk)
        except Exception as err:
            response['error'] = str(err)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CommissionSettingsViewSet(mixins.RetrieveModelMixin,
                                mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    '''
    @class CommissionSettingsViewSet
    @brief
        ViewSet class for CommissionSettings
        Handles HTTP requests GET, POST, PUT
    '''

    queryset = CommissionSettings.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = CommissionSettingsSerializer
    pagination_class = ESPagination

    '''
    @brief data structure
        {
            id: 1,
            name:
            status:
            invest_least:
            deposit_fee:
            deposit_fee_max:
            withdraw_fee:
            withdraw_fee_max:
            groups: [{
                    id: # group ID
                    threshold:
                    member_num:
                    discount_rate:
                    return_rate:
                    rates: [{
                                provider: # provider ID
                                name: # provider name
                                status: # provider status
                                gametypes: [{
                                                name: # game type name
                                                status: # game status
                                                type: # game type ID
                                                rate: # commission rate- rate
                                            }]
                            }]
                    }]
        }
    '''


    def list(self, request):
        '''
        '''

        response = dict()
        try:
            commissionsettings = CommissionSettings.objects.annotate(group_count=Count('commgroup_settings'),
                                                                    member_count=Count('agent_commission_settings__member_agent'),
                                                                    agent_count=Count('agent_commission_settings'))

            # uncomment the next LOCs line if filter and pagination are supported.
            # commissionsettings = self.filter_queryset(commissionsettings)
            # commissionsettings = self.paginate_query(commissionsettings)

            serializer = CommissionSettingsForListSerializer(commissionsettings,
                                                            context={'request': request},
                                                            many=True)

            return Response(serializer.data)
        except Exception as err:
            response['error']  = err
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk):
        '''
        '''

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        for group in data.get('groups'):
            new_rates = list()
            new_rate = dict()
            rates = group['rates']

            for rate in rates:
                provider = rate['provider']
                type_cpy = rate['type'].copy()
                type_cpy['rate'] = rate['rate']

                if 'provider' in new_rate and new_rate['provider'] == provider['provider']:
                    new_rate['gametypes'].append(type_cpy)
                else:
                    new_rate = rate['provider'].copy()
                    new_rate['gametypes'] = [type_cpy]
                    if new_rate:
                        new_rates.append(new_rate)

            group['rates'] = new_rates

        return Response(data)

    def create(self, request):
        '''
        '''

        return self.__update_create(request)

    def update(self, request, pk):
        '''
        '''

        return self.__update_create(request, pk)

    def __update_create(self, request, pk=None):
        '''
        '''

        response = dict()

        data = self.request.data

        commissionsettings_dict = dict()
        commissionsettings_field = [
                                    'name',
                                    'status',
                                    'invest_least',
                                    'deposit_fee',
                                    'deposit_fee_max',
                                    'withdraw_fee',
                                    'withdraw_fee_max',
                                    ]
        for field in commissionsettings_field:
            if data.get(field) is not None:
                commissionsettings_dict[field] = data.get(field)

        commissiongroups = data.get('groups')
        if commissiongroups is not None:
            data.pop('groups')

        try:
            temp_dict = dict()
            if pk:
                # If the object is not found, this will raise an error
                commissionsetting = CommissionSettings.objects.get(pk=pk)
                temp_dict = commissionsetting.__dict__.copy()
                temp_dict.pop('_state')
                temp_dict.update(commissionsettings_dict)
                commissionsettings_dict = temp_dict
            else:
                commissionsetting = CommissionSettings(**commissionsettings_dict)

            serializer = CommissionSettingsSerializer(commissionsetting,
                                                        data=commissionsettings_dict,
                                                        context={'request': request})

            if not serializer.is_valid():
                response['error'] = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            # create or update the groups
            if commissiongroups is not None:
                # clear the relationship to the groups
                commissionsetting.commgroup_settings.clear()
                for group in commissiongroups:
                    group_dict = {
                                    'threshold': group['threshold'],
                                    'member_num': group['member_num'],
                                    'discount_rate': group['discount_rate'],
                                    'return_rate': group['return_rate']
                                    }
                    if group.get('id'):
                        group_obj = CommissionGroup.objects.get(pk=group['id'])
                        group_obj.commissionrate_group.clear()
                        for key, val in group_dict.iteritems():
                            setattr(group_obj, key, val)
                        group_obj.save()
                        commissionsetting.commgroup_settings.add(group_obj)
                    else:
                        group_obj = commissionsetting.commgroup_settings.create(**group_dict)

                    # create/update rate
                    rates = group.get('rates')
                    if rates:
                        for rate in rates:
                            rate_cpy = rate.copy()
                            rate_cpy.pop('name')
                            rate_cpy.pop('status')

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
            if response:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            response['error'] = 'CommissionSettings with id={0} not found'.format(pk)
        except Exception as err:
            response['error'] = str(err)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
