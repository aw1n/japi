import django_filters
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters, mixins, status, viewsets

from .models import RemitInfo, Transaction
from .serializers import TransactionSerializer
from tracker.mixins import LoggingMixin


class RemitInfoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                   mixins.ListModelMixin, mixins.UpdateModelMixin, 
                   LoggingMixin, viewsets.GenericViewSet):

    model = Transaction
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # serializer_class = RemitInfoSerializer
    
