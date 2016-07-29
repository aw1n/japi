import django_filters
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters, mixins, status, viewsets
from account.filters import AgentFilter, MemberFilter
from account.models import Agent, Member, AgentLevel
from account.serializers import (AgentSerializer, MemberSerializer, 
                                 AgentApplicationSerializer, MemberApplicationSerializer,
                                 MemberGuestSerializer, AgentLevelSerializer)
from bank.models import Bank
from tracker.mixins import LoggingMixin

class AgentLevelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    model = AgentLevel
    serializer_class = AgentLevelSerializer
    queryset = AgentLevel.objects.all()


class AgentViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                   mixins.ListModelMixin, mixins.UpdateModelMixin, 
                   LoggingMixin, viewsets.GenericViewSet):

    model = Agent
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    filter_class = AgentFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)
    lookup_fields = ('real_name', 'username')


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
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_class = MemberFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)


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
