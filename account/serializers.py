import datetime
from rest_framework import serializers
from account.models import (Agent, Member,
							AgentApplication)
from bank.models import BankingInfo
from level.models import Level
from settings.models import CommissionSettings, ReturnSettings

class AgentSerializer(serializers.ModelSerializer):
	'''
	@class AgentSerializer
	@brief
		Serializer for Agent
	'''

	def __init__(self, *args, **kwargs):
	    '''
	    '''

	    super(AgentSerializer, self).__init__(*args, **kwargs)
	    opt_fields = self.context['request'].query_params.get('opt_fields')
	    if opt_fields:
	        opt_fields = opt_fields.split(',')
	        # Remove not specified fields
	        to_show = set(opt_fields)
	        default = set(self.fields.keys())
	        for field in default - to_show:
	            self.fields.pop(field)


	username 				= serializers.CharField(required=False, max_length=100)
	status 					= serializers.IntegerField(required=False, default=1)
	commission_settings 	= serializers.PrimaryKeyRelatedField(required=False,queryset=CommissionSettings.objects.all())
	default_member_lv 		= serializers.PrimaryKeyRelatedField(required=False,queryset=Level.objects.all())
	default_return_settings = serializers.PrimaryKeyRelatedField(required=False,queryset=ReturnSettings.objects.all())
	level 					= serializers.IntegerField(required=False)
	parent_agent 			= serializers.PrimaryKeyRelatedField(required=False,queryset=Agent.objects.all())
	real_name 				= serializers.CharField(max_length=100, required=False)
	phone 					= serializers.CharField(max_length=50, required=False)
	gender 					= serializers.CharField(max_length=1,required=False)
	birthday 				= serializers.DateField(required=False)
	email					= serializers.EmailField(required=False)
	wechat					= serializers.CharField(max_length=255, required=False)
	qq						= serializers.CharField(max_length=255, required=False)
	memo					= serializers.CharField(required=False)
	bank 					= serializers.PrimaryKeyRelatedField(required=False,queryset=BankingInfo.objects.all())	

	class Meta:
		model = Agent
		# fields = ('username','status','email')

	def validate(self, data):
		request = self.context['request']

		if request.method == 'POST':
			if 'username' in data:
				if Agent.objects.filter(username=data['username']).count():
					raise serializers.ValidationError({"detail": "Username already exists"})
		return data

class AgentApplicationSerializer(serializers.ModelSerializer):
	'''
	@class AgentApplicationSerializer
	@brief
		Serializer for Agent Application
	'''

	def __init__(self, *args, **kwargs):
	    '''
	    '''

	    super(AgentApplicationSerializer, self).__init__(*args, **kwargs)
	    opt_fields = self.context['request'].query_params.get('opt_fields')
	    if opt_fields:
	        opt_fields = opt_fields.split(',')
	        # Remove not specified fields
	        to_show = set(opt_fields)
	        default = set(self.fields.keys())
	        for field in default - to_show:
	            self.fields.pop(field)


	username		= serializers.CharField(required=False, max_length=100)
	active_account 	= serializers.PrimaryKeyRelatedField(required=False, queryset=Agent.objects.all())
	account 		= serializers.CharField(max_length=100, required=False)
	name 	 		= serializers.CharField(max_length=100, required=False)
	phone			= serializers.CharField(max_length=50, required=False)
	email			= serializers.EmailField(required=False)
	ip 				= serializers.CharField(max_length=100, required=False)
	status			= serializers.IntegerField(required=False, default=1)

	class Meta:
		model = AgentApplication
		# fields = ('username','active_account','account','name','phone','email','ip','status','confirm_at')

	def validate(self, data):
		request = self.context['request']

		if request.method == 'POST':
			if 'username' in data:
				if Agent.objects.filter(username=data['username']).count():
					raise serializers.ValidationError({"detail": "Username already exists"})
		return data



class MemberSerializer(serializers.ModelSerializer):
	'''
	@class AgentSerializer
	@brief
		Serializer for Agent
	'''
	
	def __init__(self, *args, **kwargs):
	    '''
	    '''

	    super(MemberSerializer, self).__init__(*args, **kwargs)
	    opt_fields = self.context['request'].query_params.get('opt_fields')
	    if opt_fields:
	        opt_fields = opt_fields.split(',')
	        # Remove not specified fields
	        to_show = set(opt_fields)
	        default = set(self.fields.keys())
	        for field in default - to_show:
	            self.fields.pop(field)


	username 				= serializers.CharField(required=False, max_length=100)
	real_name 				= serializers.CharField(max_length=100, required=False)
	phone 					= serializers.CharField(max_length=50, required=False)
	gender 					= serializers.CharField(max_length=1,required=False)
	email					= serializers.EmailField(required=False)
	birthday 				= serializers.DateField(required=False)
	wechat					= serializers.CharField(max_length=255, required=False)
	qq						= serializers.CharField(max_length=255, required=False)
	memo					= serializers.CharField(required=False)
	level 					= serializers.IntegerField(required=False)
	status 					= serializers.IntegerField(required=False, default=1)
	return_settings			= serializers.PrimaryKeyRelatedField(required=False,queryset=ReturnSettings.objects.all())
	level_lock				= serializers.IntegerField(required=False)
	banking_info			= serializers.PrimaryKeyRelatedField(required=False,queryset=BankingInfo.objects.all())	
	agent 					= serializers.PrimaryKeyRelatedField(required=False,queryset=Agent.objects.all())	

	class Meta:
		model = Member

	def validate(self, data):
		request = self.context['request']

		if request.method == 'POST':
			if 'username' in data:
				if Agent.objects.filter(username=data['username']).count():
					raise serializers.ValidationError({"detail": "Username already exists"})
		return data
