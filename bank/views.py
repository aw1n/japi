from rest_framework import viewsets, mixins
from .models import Bank, BankInfo
from .serializers import BankSerializer, BankInfoSerializer
from loginsvc.permissions import IsAdmin, IsAgent, IsMember
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import User, Group
from rest_condition import And, Or, Not

# Create your views here.
class BankViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    model = Bank
    permission_classes = [IsAdmin]
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

class BankInfoViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    model = BankInfo
    permission_classes = [Or(IsAdmin, IsAgent, IsMember)]
    serializer_class = BankInfoSerializer
    queryset = BankInfo.objects.all()

    def get_queryset(self):

        # for Member and agent only restricted
        # member/s can only be listed, retrieved or updated
        if self.request.method == 'GET' or self.request.method == 'PUT':
            token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')
            if token[0] != 'Bearer':
                return is_admin
            access_token = token[1]
            token_obj = AccessToken.objects.get(token=access_token)
            user_id = token_obj.user_id
            user = User.objects.get(pk=user_id)
            bank_id = user.bank
            user_groups = user.groups.all()
            if Group.objects.get(name='member_grp') in user_groups:
                return BankInfo.objects.filter(pk=bank_id)
            if Group.objects.get(name='agent_grp') in user_groups:
                return BankInfo.objects.filter(pk=bank_id)
        return self.queryset
