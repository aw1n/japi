from rest_framework import viewsets, mixins
from .models import Bank, BankInfo
from .serializers import BankSerializer, BankInfoSerializer

# Create your views here.
class BankViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    model = Bank
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

class BankInfoViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    model = BankInfo
    serializer_class = BankInfoSerializer
    queryset = BankInfo.objects.all()

   