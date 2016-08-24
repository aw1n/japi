from django.shortcuts import render
from tracker.managers import PrefetchUserManager
from tracker.serializers import TrackerSerializer, LoginRecordSerializer
from tracker.models import BaseAPIRequestLog, APIRequestLog, LoginRecord
from tracker.filters import LoginRecordFilter
from rest_framework import mixins, status, viewsets, filters
from rest_framework import generics
from rest_framework.response import Response


class LoggingViewSet( mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                    mixins.ListModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    model = APIRequestLog
    queryset = APIRequestLog.objects.all()
    serializer_class = TrackerSerializer
    # pass


class LoginRecordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    '''

    model = LoginRecord
    permission_classes = []
    queryset = LoginRecord.objects.all()
    serializer_class = LoginRecordSerializer
    filter_class = LoginRecordFilter
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('ipaddr')
