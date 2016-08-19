from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from transaction.models import RemitInfo, Transaction, OnlinePayee, Balance, PaymentType, TransactionType
from account.models import Member
from level.models import Level

# class TransactionTestCase(APITestCase):

#     def test_remitinfo_can_create(self):
#         url = '/api/remitinfo/'
#         data = {
#             'bank': 'Metrobank',
#             'way': 'adsfasdf',
#             'depositor': 'Raphael Torres',
#             'amount': 10.50
#         }
#         response = self.client.post(url, data, format='json')
#         print response.data
        # self.assertEqual(response.data, 1)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'Metrobank')


class OnlinePaymentTest(APITestCase):
    '''
    '''

    fixtures = ['onlinepayment_test.json', 'transactiontype.json']


    def test_onlinepayment_001(self):
        '''
        '''

        member = Member.objects.get(real_name='Real Name')
        onlinepayment_data = {
                                'amount': 1500,
                                'member_id': member.pk,
                                'merchant_num': 1
                            }

        response = self.client.post('http://127.0.0.1:8000/api/onlinepayment/',
                                onlinepayment_data)

        self.assertEqual(response.status_code, 201)

    def test_onlinepayment_002(self):
        '''
        '''

        member = Member.objects.get(real_name='Real Name')
        onlinepayment_data = {
                                'amount': 999,
                                'member_id': member.pk,
                                'merchant_num': 1
                            }

        response = self.client.post('http://127.0.0.1:8000/api/onlinepayment/',
                                onlinepayment_data)

        self.assertEqual(response.status_code, 400)

    def test_onlinepayment_003(self):
        '''
        '''

        member = Member.objects.get(real_name='Real Name')
        onlinepayment_data = {
                                'amount': 10001,
                                'member_id': member.pk,
                                'merchant_num': 1
                            }

        response = self.client.post('http://127.0.0.1:8000/api/onlinepayment/',
                                onlinepayment_data)

        self.assertEqual(response.status_code, 400)

    def test_onlinepayment_004(self):
        '''
        '''

        member = Member.objects.get(real_name='Real Name')
        onlinepayment_data = {
                                'amount': 1000,
                                'member_id': member.pk,
                                'merchant_num': 1
                            }

        response = self.client.post('http://127.0.0.1:8000/api/onlinepayment/',
                                onlinepayment_data)

        self.assertEqual(response.status_code, 201)

    def test_onlinepayment_005(self):
        '''
        '''

        member = Member.objects.get(real_name='Real Name')
        onlinepayment_data = {
                                'amount': 10000,
                                'member_id': member.pk,
                                'merchant_num': 1
                            }

        response = self.client.post('http://127.0.0.1:8000/api/onlinepayment/',
                                onlinepayment_data)

        self.assertEqual(response.status_code, 201)
