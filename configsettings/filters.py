from rest_framework import filters
from configsettings.models import Discount, ReturnGroup, ReturnSettings
import django_filters


class DiscountFilter(filters.FilterSet):
    '''
    @class DiscountFilter
    @brief
        Filter class for Discount model
    '''

    type = django_filters.CharFilter(name='type', lookup_type='exact')

    class Meta:
        model = Discount
        fields = ['type']


class ReturnRateConfigFilter(filters.FilterSet):
    '''
    @class ReturnRateConfigFilter
    @brief
        Filter class for ReturnRateConfig model
    '''

    provider = django_filters.CharFilter(name='provider__name', lookup_type='exact')
    type = django_filters.CharFilter(name='type__name', lookup_type='exact')

    class Meta:
        model = ReturnGroup
        fields = ['provider', 'type']


class ReturnSettingsFilter(filters.FilterSet):
    '''
    @class ReturnSettingsFilter
    @brief
        Filter class for ReturnSettings model
    '''

    name = django_filters.CharFilter(name='name', lookup_type='exact')
    status = django_filters.CharFilter(name='status', lookup_type='exact')

    class Meta:
        model = ReturnSettings
        fields = ['name', 'status']
