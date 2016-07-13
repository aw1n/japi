import django_filters
from django.http import Http404
from rest_framework import filters
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import mixins, status, viewsets
from account.filters import AgentFilter
from account.models import Agent, Member, AgentApplication
from account.serializers import AgentSerializer, AgentRetrieveSerializer, MemberSerializer, AgentApplicationSerializer
from bank.models import Bank


class AgentViewSet( mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                    mixins.ListModelMixin, mixins.UpdateModelMixin, 
                    viewsets.GenericViewSet):
    '''
    @class AgentViewSet
    @brief
        Viewset for agent
    '''
    
    model = Agent
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()
    filter_class = AgentFilter
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)
    # filter_fields = ('username',
    #                   'register_at',
    #                   'status',
    #                   'commission_settings',
    #                   'default_return_settings',
    #                   'level',
    #                   'parent_agent',
    #                   'promo_code',
    #                   'gender',
    #                   'real_name',
    #                   'phone',
    #                   'email',
    #                   'wechat',
    #                   'qq',
    #                   'bank',
    #                   'account')

    # def list(self, request):
    #     response = {}
    #     queryset = Agent.objects.all()
    #     serializer = AgentRetrieveSerializer(queryset, context={"request":request}, many=True)
    #     response['status_code'] = status.HTTP_200_OK
    #     response['data'] = serializer.data
    #     return Response(response)

    def retrieve(self, request, pk=None):
        try:
            queryset = Agent.objects.get(pk=pk)
            serializer = AgentRetrieveSerializer(queryset)
            response = {}
            response['status_code'] = status.HTTP_200_OK
            response['data'] = serializer.data
            return Response(response)
        except Agent.DoesNotExist:
            raise Http404

    def update(self, request, pk, format=None):
        response = {}

        try:
            agent = Agent.objects.get(id=pk)
            serializer = AgentSerializer(agent, data=request.data, context={'request': request}, partial=True)

            if serializer.is_valid():
                serializer.save()
                response['status_code'] = status.HTTP_200_OK
                response['data'] = serializer.data
                return Response(response)

            response['status_code'] = status.HTTP_400_BAD_REQUEST
            response['error'] = serializer.errors
            return Response(response)
        except Agent.DoesNotExist:
            raise Http404

class AgentApplicationViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                              mixins.ListModelMixin, mixins.UpdateModelMixin, 
                              viewsets.GenericViewSet):
    '''
    @class AgentApplicationViewSet
    @brief
        Viewset for agent application
    '''
    
    model = AgentApplication
    serializer_class = AgentApplicationSerializer
    queryset = AgentApplication.objects.all()

    def update(self, request, pk, format=None):
        response = {}

        try:
            agent = AgentApplication.objects.get(id=pk)
            serializer = AgentApplicationSerializer(agent, data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            response['error'] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except AgentApplication.DoesNotExist:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class MemberViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    @class MemberViewSet
    @brief
        Viewset for member
    '''

    model = Member
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

    # def retrieve(self, request, pk=None):
    #     queryset = Member.objects.all()
    #     member = get_object_or_404(queryset, pk=pk)
    #     serializer = MemberSerializer(member)
    #     return Response(serializer.data)

    # def list(self, request):
    #     response = {}
    #     queryset = Member.objects.all()
    #     serializer = MemberSerializer(queryset, context={"request":request}, many=True)
    #     response['status_code'] = status.HTTP_200_OK
    #     response['data'] = serializer.data
    #     return Response(response)

    def update(self, request, pk, format=None):
        response = {}

        try:
            member = Member.objects.get(id=pk)
            serializer = MemberSerializer(member, data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            response['error'] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            raise Http404
