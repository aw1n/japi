from django.shortcuts import render
from tracker.managers import PrefetchUserManager
from tracker.serializers import TrackerSerializer
from tracker.models import BaseAPIRequestLog, APIRequestLog
from rest_framework import mixins, status, viewsets
from rest_framework import generics
from rest_framework.response import Response


class LoggingViewSet( mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                    mixins.ListModelMixin, mixins.UpdateModelMixin, 
                    viewsets.GenericViewSet):
    model = APIRequestLog
    queryset = APIRequestLog.objects.all()
    serializer_class = TrackerSerializer
    # pass