from rest_framework import renderers, viewsets, mixins, status, filters, parsers
from rest_framework.response import Response
from django.core import serializers
from django.http import Http404
from configsettings.serializers import DiscountSerializer, ReturnSettingsSerializer, ReturnRateConfigSerializer, RateConfigRetrieveSerializer, CommissionSettingsSerializer
from configsettings.filters import DiscountFilter
from configsettings.models import Discount, ReturnSettings, ReturnRateConfig
from configsettings.filters import DiscountFilter
from configsettings.models import Discount, CommissionSettings
from jaguar.utils import ESPagination
from provider.models import Provider
from gametype.models import GameType

import django_filters


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


class ReturnRateConfigViewSet(mixins.RetrieveModelMixin,
                                mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    '''
    @class ReturnRateConfigViewSet
    @brief
        View set for ReturnRateConfig model
        Handles HTTP requests such as POST, GET, PUT
    '''

    queryset = ReturnRateConfig.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = ReturnRateConfigSerializer

    def get_serializer_class(self):
        '''
        '''

        if self.request.method == 'GET':
            return RateConfigRetrieveSerializer
        elif self.request.method == 'POST':
            return self.serializer_class

    def create(self, request):
        '''
        '''

        config_fields = ['provider', 'type', 'rate', 'threshold', 'max', 'check_amount', 'return_setting']
        data_dict = dict()
        response = dict()

        for field in config_fields:
            if request.data.get(field) is not None:
                data_dict[field] = request.data.get(field)
        try:
            # get foreign key fields
            provider_arg = self.request.data.get('provider')
            return_setting_arg = self.request.data.get('return_setting')
            gametype_arg = self.request.data.get('type')

            if provider_arg:
                provider = Provider.objects.get(name=provider_arg)
                data_dict['provider'] = provider.pk
            if gametype_arg:
                gametype = GameType.objects.get(name=gametype_arg)
                data_dict['type'] = gametype.pk
            if return_setting_arg:
                return_setting = ReturnSettings.objects.get(pk=return_setting_arg)
                data_dict['return_setting'] = return_setting.pk

            returnrateconfig = ReturnRateConfig()
            serializer = self.get_serializer_class(returnrateconfig,
                                                    data=data_dict,
                                                    context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            response['error'] = serializer.errors
        except Exception as err:
            response['error'] = err
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

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


    def create(self, request):
        '''
        '''

        # Parse ReturnSettings fields name, status
        returnsettings_dict = dict()
        data_dict = self.request.data
        returnsettings_dict['name'] = data_dict.get('name')
        if data_dict.get('status'):
            returnsettings_dict['status'] = data_dict.get('status')

        returnrateconfigs = list()

        for config in data_dict.get('configs'):
            config_dict = dict()
            # get threshold - REQUIRED
            config_dict['threshold'] = config.get('threshold')
            # get max
            config_dict['max'] = config.get('max')
            # get check_amount
            config_dict['check_amount'] = config.get('check_amount')

            # loop through providers
            for provider in config.get('providers'):
                temp_dict = config_dict.copy()
                provider_dict = dict()
                # get provider's name
                provider_dict['provider'] = provider.get('provider')
                temp_dict.update(provider_dict)

                #loop throuhg rate_configs
                for rate_config in provider.get('rate_configs'):
                    temp_rate_dict = temp_dict.copy()
                    # get type
                    # get rate
                    temp_rate_dict.update(rate_config)
                    returnrateconfigs.append(temp_rate_dict)
        response = dict()

        try:
            returnsettings = ReturnSettings(**returnsettings_dict)
            serializer = ReturnSettingsSerializer(returnsettings,
                                                    data=returnsettings_dict,
                                                    context={'request': request,
                                                             'returnrateconfigs': returnrateconfigs})
            if not serializer.is_valid():
                response['error'] = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            # print('XXXXXXXXXXXXXXXXXXXX')
            # returnsettings.returnrate_settings.clear()
            # for rateconfig in returnrateconfigs:
            #     # Update rateconfig content
            #     # Provider, type should be instances
            #     if not rateconfig.get('id'):
            #         # create returnrateconfig
            #         returnrateconfig = returnsettings.returnrate_settings.create(**rateconfig)
            #         returnrateconfig.save()
            #         continue
            #     # update existing returnrateconfig
            #     to_update = ReturnRateConfig.objects.get(pk=rateconfig.get('id'))
            #     for key, value in rateconfig.iteritems():
            #         setattr(to_update, key, value)
            #     to_update.save()
            #     # add to return settings
            #     returnsettings.returnrate_settings.add(to_update)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            response['error'] = err
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CommissionSettingsViewSet(mixins.RetrieveModelMixin, 
                                mixins.CreateModelMixin, 
                                mixins.ListModelMixin, 
                                mixins.UpdateModelMixin, 
                                viewsets.GenericViewSet):
    
    model = CommissionSettings
    serializer_class = CommissionSettingsSerializer
    queryset = CommissionSettings.objects.all()
