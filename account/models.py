from __future__ import unicode_literals
from django.db import models

from level.models import Level
from settings.models import ReturnSettings, CommissionSettings
from bank.models import BankingInfo

AGENT_STATUS_OPTIONS = (
	('0', 'Suspended'),
	('1', 'Active')
)

AGENT_APPLICATION_STATUS_OPTIONS = (
	('0', 'Rejected'),
	('1', 'Accepted')
)

AGENT_LEVEL_OPTIONS = (
	('1', 'General Holder'),
	('2', 'Holder'),
	('3', 'General Agency'),
	('4', 'Agency'),
)

MEMBER_STATUS_OPTIONS = (
	('0', 'Suspended'),
	('1', 'Active'),
	('2', 'Fund Freezed')
)

MEMBER_APPLICATION_STATUS_OPTIONS = (
	('0', 'Rejected'),
	('1', 'Accepted'),
	('2', 'Unhandled')
)

LEVEL_LOCK_OPTIONS = (
	('0', 'Locked'),
	('1', 'Unlocked')
)

GENDER_OPTIONS = (
	('M', 'Male'),
	('F', 'Female')
)

class Agent(models.Model):
	'''
	@class Agent
	@brief
		Agent model class
	'''

	id                      = models.AutoField(primary_key=True)
	username                = models.CharField(unique=True, max_length=100)
	register_at             = models.DateTimeField(auto_now=False, auto_now_add=True)
	status                  = models.IntegerField(default=1, null=True, blank=True, choices=AGENT_STATUS_OPTIONS)
	commission_settings     = models.OneToOneField(CommissionSettings, null=True, blank=True, related_name="agent_commission_settings")
	default_member_lv       = models.OneToOneField(Level, null=True, blank=True,related_name="agent_default_level")
	default_return_settings = models.OneToOneField(ReturnSettings, null=True, blank=True, related_name="agent_default_return_settings")
	level                   = models.IntegerField(default=1, choices=AGENT_LEVEL_OPTIONS)
	parent_agent            = models.ForeignKey('self', related_name='children', null=True, blank=True)
	real_name               = models.CharField(max_length=100)
	phone                   = models.CharField(max_length=50)
	gender                  = models.CharField(max_length=1, choices=GENDER_OPTIONS)
	birthday                = models.DateField(blank=True, null=True)
	email                   = models.EmailField(max_length=70, blank=True, null=True, unique=True, default=None)
	wechat                  = models.CharField(max_length=255)
	qq                      = models.CharField(max_length=255, null=True, blank=True)
	memo                    = models.TextField(null=True, blank=True)
	bank                    = models.ForeignKey(to=BankingInfo, null=True, blank=True,related_name="agent_banking_info")

	class Meta:
		db_table = "account_agent"

class AgentApplication(models.Model):
	'''
	@class Agent application
	@brief
		Agent application model class
	'''

	id              = models.AutoField(primary_key=True)
	username        = models.CharField(unique=True, max_length=100)
	active_account  = models.OneToOneField(Agent, null=True, blank=True,related_name="agent_application")
	account         = models.CharField(max_length=255)
	name            = models.CharField(max_length=100)
	phone           = models.CharField(max_length=50)
	email           = models.EmailField(max_length=70, null=True, blank=True, unique=True, default=None)
	ip              = models.CharField(max_length=100)
	status          = models.IntegerField(default=1, null=True, blank=True, choices=AGENT_APPLICATION_STATUS_OPTIONS)
	applied_at      = models.DateTimeField(auto_now=False, auto_now_add=True)
	confirm_at      = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)

	class Meta:
		db_table = "account_agent_application"


class Member(models.Model):
	'''
	@class Member
	@brief
		Member model class
	'''

	id              = models.AutoField(primary_key=True)
	username        = models.CharField(unique=True, max_length=100)
	real_name       = models.CharField(max_length=100, blank=True, null=True)
	phone           = models.CharField(max_length=50, blank=True, null=True)
	gender          = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_OPTIONS)
	email           = models.EmailField(max_length=70, blank=True, null=True, unique=True, default=None)
	birthday        = models.DateField(blank=True, null=True)
	wechat          = models.CharField(max_length=255, blank=True, null=True)
	qq              = models.CharField(max_length=255, blank=True, null=True)
	register_at     = models.DateTimeField(auto_now=False, auto_now_add=True)
	memo            = models.TextField(null=True, blank=True)
	level           = models.OneToOneField(Level, null=True, blank=True, related_name="member_level")
	status          = models.IntegerField(default=1, choices=MEMBER_STATUS_OPTIONS)
	return_settings = models.OneToOneField(ReturnSettings, null=True, blank=True, related_name="member_return_settings")
	level_lock      = models.IntegerField(default=1, choices=LEVEL_LOCK_OPTIONS)
	banking_info    = models.OneToOneField(BankingInfo, null=True, blank=True, related_name="member_banking_info")
	agent           = models.OneToOneField(Agent, null=True, blank=True, related_name="member_agent")

	class Meta:
		db_table = "account_member"


class MemberApplication(models.Model):
	'''
	@class Member
	@brief
		Member model class
	'''

	id 				= models.AutoField(primary_key=True)
	phone           = models.CharField(max_length=50, blank=True, null=True)
	ip              = models.CharField(max_length=100)
	applied_at      = models.DateTimeField(auto_now=False, auto_now_add=True)
	status          = models.IntegerField(default=1, null=True, blank=True, choices=MEMBER_APPLICATION_STATUS_OPTIONS)
	confirm_at      = models.DateTimeField(auto_now=False, auto_now_add=True)
	username        = models.CharField(max_length=100)
	password        = models.CharField(max_length=100)

	class Meta:
		db_table = "account_member_application"

