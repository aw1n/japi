from rest_framework import renderers, viewsets, mixins, status, filters, parsers
from rest_framework.response import Response
from django.core import serializers
from django.http import Http404
from django.db.models import Count
from level.serializers import LevelSerializer
from level.filters import LevelFilter
from level.models import Level
from jaguar.utils import ESPagination
from configsettings.models import Discount

from django.contrib import admin
admin.autodiscover()
from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

import django_filters
import json
import ast
import collections


class LevelViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    '''
    @class LevelViewSet
    @brief
        View set for Level model
        Handles HTTP requests such as POST, GET, PUT
    '''

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Level.objects.all()
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = LevelSerializer
    filter_class = LevelFilter
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'status')
    pagination_class = ESPagination


    def list(self, request):
        '''
        @fn list
        @brief
            Overrides the list method (GET). This also filters the queryset
            by the parameters given by the user
        '''

        levels = Level.objects.all()

        levels = self.filter_queryset(levels.annotate(member_count=Count('member_level', distinct=True)))
        paginated_level = self.paginate_queryset(levels)
        serializer = LevelSerializer(paginated_level,
                                        context={'request': request},
                                        many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
