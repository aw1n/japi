#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import Member, Agent
