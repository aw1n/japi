from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from level.models import Level
from configsettings.models import ReturnSettings, CommissionSettings
from bank.models import BankInfo

STATUS_OPTIONS = (
	(0, 'Rejected'),
	(1, 'Active'),
	(2, 'Inactive'),
	(3, 'Pending')
)

AGENT_APPLICATION_STATUS_OPTIONS = (
	(0, 'Rejected'),
	(1, 'Accepted')
)

MEMBER_STATUS_OPTIONS = (
	(0, 'Suspended'),
	(1, 'Active'),
	(2, 'Fund Freezed')
)

MEMBER_APPLICATION_STATUS_OPTIONS = (
	(0, 'Rejected'),
	(1, 'Accepted'),
	(2, 'Unhandled')
)

LEVEL_LOCK_OPTIONS = (
	(0, 'Locked'),
	(1, 'Unlocked')
)

GENDER_OPTIONS = (
	('M', 'Male'),
	('F', 'Female')
)

class AgentLevel(models.Model):
	'''
	@class Level
	@brief
		Agent levels, by defaults we have 4 different levels by level type.
		The level of member's agent can only be 4(the lowest level).
	'''

	level = models.IntegerField(null=False, blank=False)
	name = models.CharField(max_length=50, null=False, blank=False)
	class Meta:
		db_table = 'account_level'

class Agent(models.Model):
	'''
	@class Agent
	@brief
		Agent model class
	'''

	user = models.OneToOneField(User, null=True, blank=True, related_name='agent_user')
	username = models.CharField(unique=True, max_length=100, blank=True, null=True)
	real_name = models.CharField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	gender = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_OPTIONS)
	birthday = models.DateField(blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	email = models.EmailField(max_length=70, blank=True, null=True, default=None)
	wechat = models.CharField(max_length=255, blank=True, null=True)
	qq = models.CharField(max_length=255, null=True, blank=True)
	memo = models.TextField(null=True, blank=True)
	status = models.IntegerField(default=1, null=True, blank=True, choices=STATUS_OPTIONS)
	level = models.ForeignKey(AgentLevel, null=False, blank=False, related_name='agent_level')
	promo_code = models.CharField(max_length=255, blank=True, null=True)
	parent_agent = models.ForeignKey('self', related_name='children', null=True, blank=True)
	bank = models.ForeignKey(BankInfo, null=True, blank=True,related_name='agent_banking_info')
	commission_settings = models.ForeignKey(CommissionSettings, null=True, blank=True, related_name="agent_commission_settings")
	default_member_lv = models.ForeignKey(Level, null=True, blank=True,related_name="agent_default_level")
	default_return_settings = models.ForeignKey(ReturnSettings, null=True, blank=True, related_name="agent_default_return_settings")
	referring_url = models.CharField(max_length=255, blank=True, null=True)
	initiated_by = models.CharField(max_length=255, blank=True, null=True)
	ip = models.CharField(max_length=255, blank=True, null=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	created_by = models.ForeignKey(User,related_name="agent_created_by", null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
	updated_by = models.ForeignKey(User,related_name="agent_updated_by", null=True, blank=True)

	class Meta:
		db_table = 'account_agent'


class Member(models.Model):
	'''
	@class Member
	@brief
		Member model class
	'''

	user = models.OneToOneField(User, null=True, blank=True, related_name='member_user')
	username = models.CharField(unique=True, null=True, blank=True, max_length=100)
	real_name = models.CharField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	gender = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_OPTIONS)
	email = models.EmailField(max_length=70, blank=True, null=True, default=None)
	birthday = models.DateField(blank=True, null=True)
	wechat = models.CharField(max_length=255, blank=True, null=True)
	qq = models.CharField(max_length=255, blank=True, null=True)
	memo = models.TextField(null=True, blank=True)
	level = models.ForeignKey(Level, null=True, blank=True, related_name='member_level')
	status = models.IntegerField(default=1, null=True, blank=True, choices=STATUS_OPTIONS)
	return_settings = models.ForeignKey(ReturnSettings, null=True, blank=True, related_name='member_return_settings')
	level_lock = models.IntegerField(default=1, choices=LEVEL_LOCK_OPTIONS)
	bank = models.ForeignKey(BankInfo, null=True, blank=True, related_name='member_banking_info')
	agent = models.ForeignKey(Agent, null=True, blank=True, related_name='member_agent')
	referring_url = models.CharField(max_length=255, blank=True, null=True)
	initiated_by = models.CharField(max_length=255, blank=True, null=True)
	ip = models.CharField(max_length=255, blank=True, null=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	created_by = models.ForeignKey(User,related_name="member_created_by", null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
	updated_by = models.ForeignKey(User,related_name="member_updated_by", null=True, blank=True)

	class Meta:
		db_table = 'account_member'

