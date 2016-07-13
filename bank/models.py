from __future__ import unicode_literals

from django.db import models

STATUS_OPTIONS = (
    ('0', 'Inactive'),
    ('1', 'Active')
)

class Bank(models.Model):
	'''
	@class Bank
	@brief
		Bank model class
	'''

	id			= models.AutoField(primary_key=True)
	bank_name	= models.CharField(max_length=100, blank=True, null=True)
	province	= models.CharField(max_length=100, blank=True, null=True)
	city		= models.CharField(max_length=100, blank=True, null=True)
	account		= models.CharField(max_length=100, blank=True, null=True)
	memo		= models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		db_table = "bank"
