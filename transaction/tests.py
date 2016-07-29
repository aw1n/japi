from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import RemitInfo

class TransactionTestCase(APITestCase):

    def test_remitinfo_can_create(self):
        url = '/api/remitinfo/'
        data = {
            'bank': 'Metrobank',
            'way': 'adsfasdf',
            'depositor': 'Raphael Torres',
            'amount': 10.50
        }
        response = self.client.post(url, data, format='json')
        print response.data
        # self.assertEqual(response.data, 1)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'Metrobank')
