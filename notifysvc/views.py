from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters, mixins, status, viewsets

# from tasks import NotifySvcTask
from account.models import Member
from transaction.models import Transaction, Balance
from jaguar.lib.paymentgateway import PaymentGateway
from tracker.mixins import LoggingMixin

class NotifySvcView(LoggingMixin, viewsets.GenericViewSet):

    def list(self, request):
        return Response('trace')

    def create(self, request):
        # notify_task = NotifySvcTask.delay()
        transaction_id = request.data.get('Billno')
        transaction = Transaction.objects.get(transaction_id=transaction_id)

        if request.data.get('Succeed') == "88":
            member = Member.objects.get(pk=transaction.member_id)
            transaction.status = 1
            transaction.save()

            try:
                balance = Balance.objects.get(member_id=transaction.member_id)
                balance.balance += request.data.get('Amount')
                balance.save()
            except:
                bal_data = {
                    'balance': request.data.get('Amount'),
                    'member_id': member.id
                }
                balance = Balance.objects.create(**bal_data)


        return Response(request.data, status=status.HTTP_200_OK)
