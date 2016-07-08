from django.shortcuts import render
from rest_framework import (mixins, status, viewsets)
from account.models import (Agent, Member,
							AgentApplication)
from account.serializers import (AgentSerializer, MemberSerializer,
								 AgentApplicationSerializer)
from django.http import Http404
from rest_framework.response import Response


class AgentViewSet(	mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
					mixins.ListModelMixin, mixins.UpdateModelMixin, 
					viewsets.GenericViewSet):
	'''
	@class AgentViewSet
	@brief
		Viewset for agent
	'''
	
	model 				= Agent
	serializer_class 	= AgentSerializer
	queryset 			= Agent.objects.all()

	def update(self, request, pk, format=None):
		response = {}

		try:
			agent = Agent.objects.get(id=pk)
			serializer = AgentSerializer(agent, data=request.data, context={'request': request})

			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)

			response['error'] = serializer.errors
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
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
	
	model 				= AgentApplication
	serializer_class 	= AgentApplicationSerializer
	queryset 			= AgentApplication.objects.all()

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
			raise Http404

class MemberViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
					mixins.ListModelMixin, mixins.UpdateModelMixin, 
					viewsets.GenericViewSet):
	'''
	@class MemberViewSet
	@brief
		Viewset for member
	'''

	model 				= Member
	serializer_class 	= MemberSerializer
	queryset 			= Member.objects.all()

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
