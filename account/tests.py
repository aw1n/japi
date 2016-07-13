# from django.test import TestCase
from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework import status

from account.models import (Member, Agent,
							MemberApplication, AgentApplication)

import unittest

class AgentTestCase(APITestCase):
	'''
	@class AgentTestCase
	@brief
		Test class for Agent model
	'''

	# def setUp(self):
	# 	# Load fixtures
	# 	call_command('loaddata', 'fixtures/test_agent.json', verbosity=0)

	#---GET METHOD---#
	def test_can_get_agent_list(self):
		a = Agent(username='test1', real_name='test1')
		a = Agent(username='test2', real_name='test2')
		a.save()

		url = '/api/agent/'
		response = self.client.get(url)
		# print response.content
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_can_get_agent_details(self):
		a = Agent(username='test1', real_name='test1')
		a.save()

		url = '/api/agent/%s/' % a.id
		response = self.client.get(url)
		# print response.content
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_can_create_agent_application_list(self):
		a = AgentApplication(username='test1', name='test1')
		a = AgentApplication(username='test2', name='test2')
		a.save()

		url = '/api/agentapplication/'
		response = self.client.get(url)
		# print response.content
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_can_create_agent_application_details(self):
		a = AgentApplication(username='test1', name='test1')
		a.save()

		url = '/api/agentapplication/%s/' % a.id
		response = self.client.get(url)
		# print response.content
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_can_get_member_list(self):
		m = Member(username='test1', real_name='test1')
		m = Member(username='test2', real_name='test2')
		m.save()

		url = '/api/member/'
		response = self.client.get(url)
		# print response.content
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	# def test_can_create_member_application_list(self):
	# 	m = MemberApplication(username='test1', password='test1')
	# 	m = MemberApplication(username='test2', password='test2')
	# 	m.save()

	# 	url = '/api/memberapplication/'
	# 	response = self.client.get(url)
	# 	# print response.content
	# 	self.assertEqual(response.status_code, status.HTTP_200_OK)


	#---POST METHOD---#
	def test_can_create_agent(self):
		url = '/api/agent/'
		data = {"username": "test1", "real_name": "test1"}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


	def test_can_create_agent_application(self):
		url = '/api/agentapplication/'
		data = {"username": "test1", "name": "test1"}
		response = self.client.post(url, data, format='json')
		# print response.content
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


	def test_can_create_member(self):
		url = '/api/member/'
		data = {"username": "test1", "real_name": "test1", "agent_id": 1}
		response = self.client.post(url, data, format='json')
		# print response.content
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


	#---PUT METHOD---#
	def test_can_update_agent(self):
		a = Agent(username='test1', real_name='test1')
		a.save()

		url = '/api/agent/%s/' % a.id
		data = {"real_name": "test111"}
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_can_update_agent_application(self):
		a = AgentApplication(username='test1', name='test1')
		a.save()

		url = '/api/agentapplication/%s/' % a.id
		data = {"status": 0}
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_can_update_member(self):
		m = Member(username='test1', real_name='test1')
		m.save()

		url = '/api/member/%s/' % m.id
		data = {"real_name": "test_member111"}
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
