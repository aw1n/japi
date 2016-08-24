import django_filters
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters, mixins, status, viewsets

from tracker.mixins import LoggingMixin
from .models import RemitInfo, RemitPayee,Transaction, PaymentType, OnlinePayee, Balance
from .serializers import (RemitInfoSerializer, RemitPayeeSerializer, TransactionSerializer,
                          PaymentTypeSerializer, OnlinePayeeSerializer, OnlinePaymentSerializer,
                          WithdrawTransactionSerializer, BalanceTransactionSerializer)


class RemitPayeeViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin,
                   LoggingMixin, viewsets.GenericViewSet):

    model = RemitPayee
    queryset = RemitPayee.objects.all()
    serializer_class = RemitPayeeSerializer


class RemitInfoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin,
                   LoggingMixin, viewsets.GenericViewSet):

    model = RemitInfo
    queryset = RemitInfo.objects.all()
    serializer_class = RemitInfoSerializer

    # model = Transaction
    # queryset = Transaction.objects.all()
    # serializer_class = TransactionSerializer


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


class OnlinePaymentViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin,
                   LoggingMixin, viewsets.GenericViewSet):

    model = Transaction
    permission_classes = []
    queryset = Transaction.objects.all()
    serializer_class = OnlinePaymentSerializer


class WithdrawTransactionViewSet(mixins.CreateModelMixin,
                   LoggingMixin, viewsets.GenericViewSet):

    model = Transaction
    permission_classes = []
    queryset = Transaction.objects.all()
    serializer_class = WithdrawTransactionSerializer


class BalanceViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                    mixins.ListModelMixin, mixins.UpdateModelMixin,
                    LoggingMixin, viewsets.GenericViewSet):
    '''
    '''

    model = Balance
    permission_classes = []
    queryset = Balance.objects.all()
    serializer_class = BalanceTransactionSerializer
