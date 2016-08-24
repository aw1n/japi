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
from loginsvc.permissions import IsAdmin, IsAgent, IsMember

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
    permission_classes = [IsAdmin]
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

    permission_classes = [IsAdmin]
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

    permission_classes = [IsAdmin]
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
