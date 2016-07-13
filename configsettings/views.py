from rest_framework import renderers, viewsets, mixins, status, filters, parsers
from rest_framework.response import Response
from django.core import serializers
from django.http import Http404
from configsettings.serializers import DiscountSerializer, CommissionSettingsSerializer
from configsettings.filters import DiscountFilter
from configsettings.models import Discount, CommissionSettings
from jaguar.utils import ESPagination
from configsettings.models import Discount

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


class CommissionSettingsViewSet(mixins.RetrieveModelMixin, 
                                mixins.CreateModelMixin, 
                                mixins.ListModelMixin, 
                                mixins.UpdateModelMixin, 
                                viewsets.GenericViewSet):
    
    model = CommissionSettings
    serializer_class = CommissionSettingsSerializer
    queryset = CommissionSettings.objects.all()

    def list(self, request):
        response = {}
        queryset = CommissionSettings.objects.all()
        serializer = CommissionSettingsSerializer(queryset, context={"request":request}, many=True)
        response['status_code'] = status.HTTP_200_OK
        response['data'] = serializer.data
        return Response(response)
