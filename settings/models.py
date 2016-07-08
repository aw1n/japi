from __future__ import unicode_literals

from django.db import models

STATUS_OPTIONS = (
    ('0', 'Inactive'),
    ('1', 'Active')
)

class ReturnSettings(models.Model):
	'''
	@class ReturnSettings
	@brief
		ReturnSettings model class
	'''

	id		= models.AutoField(primary_key=True)
	name	= models.CharField(max_length=100)
	status	= models.IntegerField(default=0, choices=STATUS_OPTIONS)

	class Meta:
		db_table = "settings_returnsettings"

class CommissionSettings(models.Model):
	'''
	@class CommissionSettings
	@brief
		CommissionSettings model class
	'''

	id					= models.AutoField(primary_key=True)
	name				= models.CharField(max_length=100)
	status				= models.IntegerField(default=0, choices=STATUS_OPTIONS)
	invest_least		= models.IntegerField() #minimum bet
	deposit_fee			= models.IntegerField() #single deposit fee
	deposit_fee_max		= models.IntegerField() #deposit fee cap
	withdraw_fee		= models.IntegerField() #single withdrawal fees
	withdraw_fee_max	= models.IntegerField() #withdrawal fee cap

	class Meta:
		db_table = "settings_commissionsettings"
