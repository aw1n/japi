import django_filters
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters, mixins, status, viewsets

from .models import RemitInfo, Transaction, PaymentType, OnlinePayee
from .serializers import TransactionSerializer, PaymentTypeSerializer, OnlinePayeeSerializer
from tracker.mixins import LoggingMixin


class RemitInfoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                   mixins.ListModelMixin, mixins.UpdateModelMixin, 
                   LoggingMixin, viewsets.GenericViewSet):

    model = Transaction
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                   mixins.ListModelMixin, mixins.UpdateModelMixin, 
                   LoggingMixin, viewsets.GenericViewSet):

    model = Transaction
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class PaymentTypeViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                   mixins.ListModelMixin, mixins.UpdateModelMixin, 
                   LoggingMixin, viewsets.GenericViewSet):

    model = PaymentType
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class OnlinePayeeViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                   mixins.ListModelMixin, mixins.UpdateModelMixin, 
                   LoggingMixin, viewsets.GenericViewSet):

    model = OnlinePayee
    queryset = OnlinePayee.objects.all()
    serializer_class = OnlinePayeeSerializer
    
