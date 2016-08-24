import django_filters
from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters, mixins, status, viewsets
from account.filters import AgentFilter, MemberFilter
from account.models import Agent, Member, AgentLevel
from account.serializers import (AgentSerializer, MemberSerializer,
                                 AgentApplicationSerializer, MemberApplicationSerializer,
                                 MemberGuestSerializer, AgentLevelSerializer, MemberRegistrationSerializer)
from bank.models import Bank
from tracker.mixins import LoggingMixin
from rest_framework import permissions
from loginsvc.permissions import IsAdmin, IsAgent, IsMember, IsUserPermitted
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import User, Group
from rest_condition import And, Or, Not

from rest_framework.decorators import api_view, permission_classes
from captcha.image import ImageCaptcha
import random
import string
import json

class AgentLevelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    model = AgentLevel
    serializer_class = AgentLevelSerializer
    queryset = AgentLevel.objects.all()


class AgentViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin,
                   LoggingMixin, viewsets.GenericViewSet):

    model = Agent
    permission_classes = [Or(IsAdmin, IsAgent, IsUserPermitted)]
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    filter_class = AgentFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)
    lookup_fields = ('real_name', 'username')

    def get_queryset(self):
        if self.request.method == 'GET' or self.request.method == 'PUT':
            token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')
            access_token = token[1]
            token_obj = AccessToken.objects.get(token=access_token)
            user_id = token_obj.user_id
            user_groups = User.objects.get(pk=user_id).groups.all()

            if Group.objects.get(name='agent_grp') in user_groups:
                return Agent.objects.filter(parent_agent=user_id) | Agent.objects.filter(user_id=user_id)
        return self.queryset


class AgentApplicationViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin,
                   LoggingMixin, viewsets.GenericViewSet):

    model = Agent
    queryset = Agent.objects.all()
    serializer_class = AgentApplicationSerializer
    filter_class = AgentFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)
    lookup_fields = ('real_name', 'username')


class MemberViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    LoggingMixin, viewsets.GenericViewSet):

    model = Member
    permission_classes = [Or(IsAdmin, IsAgent, IsUserPermitted)]
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_class = MemberFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)

    def get_queryset(self):

        # for Member and agent only restricted
        # member/s can only be listed, retrieved or updated
        if self.request.method == 'GET' or self.request.method == 'PUT':
            token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')
            access_token = token[1]
            token_obj = AccessToken.objects.get(token=access_token)
            user_id = token_obj.user_id
            user_groups = User.objects.get(pk=user_id).groups.all()
            if Group.objects.get(name='member_grp') in user_groups:
                return Member.objects.filter(user_id=user_id)
            if Group.objects.get(name='agent_grp') in user_groups:
                return Member.objects.filter(agent_id=user_id)
        return self.queryset


class MemberApplicationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    LoggingMixin, viewsets.GenericViewSet):

    model = Member
    queryset = Member.objects.all()
    serializer_class = MemberApplicationSerializer
    filter_class = MemberFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)


class MemberGuestViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    LoggingMixin, viewsets.GenericViewSet):

    model = Member
    queryset = Member.objects.all()
    serializer_class = MemberGuestSerializer
    filter_class = MemberFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)


class MemberRegistrationViewSet(mixins.CreateModelMixin, LoggingMixin, viewsets.GenericViewSet):
    '''
    @class MemberRegistrationViewSet
    @brief
        Viewset for Member Registration
    '''

    model = Member
    permission_classes = []
    queryset = Member.objects.all()
    serializer_class = MemberRegistrationSerializer

@api_view(['GET'])
@permission_classes([])
def generate_verification_code(request):
    '''
    '''

    code = random_code_generator(5)
    image = ImageCaptcha()
    image.write(code, 'captcha/{0}.png'.format(code))
    verification_code = { 'verification_image': '{0}.png'.format(code),
                            'code': code}

    return HttpResponse(json.dumps(verification_code),
                        status=200,
                        content_type='application/json')


def random_code_generator(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))