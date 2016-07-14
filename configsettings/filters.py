from rest_framework import filters
from configsettings.models import Discount
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
