from __future__ import unicode_literals

from django.db import models

STATUS_OPTIONS = (
    ('0', 'Inactive'),
    ('1', 'Active')
)

class BankingInfo(models.Model):
	'''
	@class BankingInfo
	@brief
		BankingInfo model class
	'''

	id			= models.AutoField(primary_key=True)
	bank_name	= models.CharField(max_length=100)
	province	= models.CharField(max_length=100)
	city		= models.CharField(max_length=100)
	account		= models.CharField(max_length=100)
	memo		= models.CharField(max_length=100)

	class Meta:
		db_table = "bank_bankinginfo"
