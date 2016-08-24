import uuid
import hashlib
import datetime
from rest_framework.exceptions import NotFound, ValidationError

from transaction.models import PaymentType, OnlinePayee

class PaymentGateway:

    @classmethod
    def generate_data(cls, merchant_id, obj):
        try:
            merchant = OnlinePayee.objects.get(pk=merchant_id)
            merchant_num = merchant.merchant_num
        except:
            raise NotFound('Online Payee does not exists.')
        else:
            payment_type = PaymentType.objects.get(pk=merchant.payment_type.id)
            function_name = payment_type.function_name
            generate_data = getattr(cls, function_name, cls.function_not_found)(function_name, merchant, obj)
            return generate_data

    @staticmethod
    def function_not_found(fff, merchant_num, obj):
        raise NotFound('Function {} does not exist. Please contact the Admin.'.format(fff))

    @staticmethod
    def generate_signature(data):
        if data:
            signature = hashlib.md5()
            for x in data:
                signature.update(str(x))
            return signature.hexdigest()
        else:
            raise NotFound('Cannot generate signature. No data found.')
            
    @staticmethod
    def tide_payment(function_name, merchant, obj):
        merchant_num = merchant.merchant_num
        merchant_key = merchant.certificate
        amount = obj.amount
        created_at = obj.created_at.strftime('%Y%m%d%H%M%S')
        transaction_id = obj.transaction_id
        return_url = 'http://tc378.net/api'
        advice_url = 'http://tc378.net/api/notifysvc/'

        for_sign = [merchant_num, transaction_id, amount, return_url, merchant_key]
        signature = hashlib.md5('{0}&{1}&{2}&{3}&{4}'.format(merchant_num, transaction_id, amount, return_url, merchant_key)).hexdigest()

        return {
            'AdviceURL': advice_url,
            'ReturnURL': return_url,
            'defaultBankNumber': '',
            'MerNo': merchant_num,
            'BillNo': transaction_id,
            'Amount': amount,
            'orderTime': created_at,
            'return_params': '',
            'SignInfo': signature.upper(),
            'merchant_key': merchant_key,

        }
