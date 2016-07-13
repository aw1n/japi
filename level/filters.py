from rest_framework import filters
from level.models import Level
import django_filters


class LevelFilter(filters.FilterSet):
    '''
    @class LevelFilter
    @brief
        Filter class for Level model
    '''

    name = django_filters.CharFilter(name='name', lookup_type='exact')
    status = django_filters.NumberFilter(name='status', lookup_type='exact')

    class Meta:
        model = Level
        fields = ['name', 'status']
