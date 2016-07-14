import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from account.models import (Agent, Member, AgentApplication)
from bank.models import Bank
from bank.serializers import BankSerializer
from level.models import Level
from configsettings.serializers import CommissionSettingsSerializer
from configsettings.models import CommissionSettings, ReturnSettings

class AgentRetrieveSerializer(serializers.ModelSerializer):

    bank = BankSerializer(required=False)
    commission_settings = CommissionSettingsSerializer(required=False)

    class Meta:
        model = Agent

class AgentParentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Agent
        fields = ('id', 'username', 'level')

class AgentSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):

        super(AgentSerializer, self).__init__(*args, **kwargs)
        opt_fields = self.context['request'].query_params.get('opt_fields')
        if opt_fields:
            opt_fields = opt_fields.split(',')
            # Remove not specified fields
            to_show = set(opt_fields)
            default = set(self.fields.keys())
            for field in default - to_show:
                self.fields.pop(field)

    bank = BankSerializer(required=False)
    level = serializers.IntegerField(required=True)
    birthday = serializers.DateField(required=False)
    # parent_agent = AgentParentSerializer(required=False)
    user = serializers.PrimaryKeyRelatedField(required=False,queryset=User.objects.all())
    commission_settings = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=CommissionSettings.objects.all())
    parent_agent = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Agent.objects.all())

    class Meta:
        model = Agent
        fields = ('user',
                  'username', 
                  'real_name', 
                  'birthday', 
                  'gender', 
                  'phone', 
                  'email', 
                  'wechat', 
                  'qq', 
                  'promo_code', 
                  'memo',
                  'parent_agent', 
                  'status', 
                  'register_at', 
                  'bank', 
                  'default_member_lv', 
                  'default_return_settings', 
                  'commission_settings', 
                  'level')

    def create(self, validated_data):
        bank_data = validated_data.pop('bank')
        user = User.objects.create(username=validated_data['username'])
        user.save()
        validated_data['user'] = user
        print "trace1"

        if 'id' in bank_data:
            try:
                bank_info = Bank.objects.get(pk=bank_data['id'])
                bank_info.account = bank_data['account']
                bank_info.save()
                validated_data['bank'] = bank_info
            except Bank.DoesNotExist:
                #initial data
                b = Bank.objects.create(**bank_data)
                validated_data['bank'] = b
        else:
            b = Bank.objects.create(**bank_data)
            validated_data['bank'] = b

        agent = Agent.objects.create(**validated_data)
        return agent

    def update(self, instance, validated_data):
        bank_data = validated_data.pop('bank')
        bank = instance.bank

        if 'id' in bank_data:
            try:
                if bank.id == bank_data['id']:
                    bank_info = Bank.objects.get(pk=bank.id)
                    bank.bank_name = bank_data.get('bank_name',bank.bank_name)
                    bank.province = bank_data.get('province',bank.province)
                    bank.city = bank_data.get('city',bank.city)
                    bank.account = bank_data.get('account',bank.account)
                    bank.memo = bank_data.get('memo',bank.memo)
                    bank.save()
                else:
                    raise serializers.ValidationError({"detail": "The Bank ID(%s) provided does not belong to this agent." % bank_data['id']})
            except Bank.DoesNotExist:
                #initial data
                b = Bank.objects.create(**bank_data)
                instance.bank = b
        else:
            b = Bank.objects.create(**bank_data)
            instance.bank = b

        instance.real_name = validated_data.get('real_name', instance.real_name)
        instance.save()
        return instance


    def validate(self, data):
        request = self.context['request']

        if request.method == 'POST':
            if 'username' in data:
                if Agent.objects.filter(username=data['username']).count():
                    raise serializers.ValidationError({"detail": "Username already exists"})

            if data['level'] == 1:
                if data['parent_agent']:
                    raise serializers.ValidationError({"detail": "Parent agent is not needed in creating Level 1 Agent."})

            if data['level'] != 1:
                if data['parent_agent'] == None:
                    raise serializers.ValidationError({"detail": "Parent ID is required."})
                else:
                    p_agent = Agent.objects.get(pk=data['parent_agent'].id)
                    if int(p_agent.level) >= data['level']:
                        raise serializers.ValidationError({"detail": "You(%s) are only allowed to create a level %s agent" % (p_agent.level,data['level'])})
            #     p_agent = Agent.objects.get(pk=data['parent_agent'].id)
            #     if int(data['level']) <= int(p_agent.level):
            #         raise serializers.ValidationError({"detail": "You(%s) are only allowed to create a level %s agent" % (p_agent.level,data['level'])})
            
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


    username = serializers.CharField(max_length=100, required=True)
    active_account = serializers.PrimaryKeyRelatedField(required=False, queryset=Agent.objects.all())
    account = serializers.CharField(max_length=100, required=False)
    name = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=50, required=False)
    email = serializers.EmailField(required=False)
    ip = serializers.CharField(max_length=100, required=True)
    status = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = AgentApplication
        # fields = ('username','active_account','account','name','phone','email','ip','status','confirm_at')

    def validate(self, data):
        request = self.context['request']

        if request.method == 'POST':
            if 'username' in data:
                if AgentApplication.objects.filter(username=data['username']).count():
                    raise serializers.ValidationError({"detail": "Username already exists."})
        return data



class MemberSerializer(serializers.ModelSerializer):
    '''
    @class MemberSerializer
    @brief
        Serializer for Member
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

    bank = BankSerializer(required=False)
    user = serializers.PrimaryKeyRelatedField(required=False,queryset=User.objects.all())
    # username = serializers.CharField(required=False, max_length=100)
    # real_name = serializers.CharField(max_length=100, required=False)
    # phone = serializers.CharField(max_length=50, required=False)
    # gender = serializers.CharField(max_length=1,required=False)
    # email = serializers.EmailField(required=False)
    # birthday = serializers.DateField(required=False)
    # wechat = serializers.CharField(max_length=255, required=False)
    # qq = serializers.CharField(max_length=255, required=False)
    # memo = serializers.CharField(required=False)
    # level = serializers.IntegerField(required=False)
    # status = serializers.IntegerField(required=False, default=1)
    # return_settings = serializers.PrimaryKeyRelatedField(required=False,queryset=ReturnSettings.objects.all())
    # level_lock = serializers.IntegerField(required=False)
    # banking_info = serializers.PrimaryKeyRelatedField(required=False,queryset=Bank.objects.all()) 
    # agent = serializers.PrimaryKeyRelatedField(required=False,queryset=Agent.objects.all())   

    class Meta:
        model = Member


    def create(self, validated_data):
        bank_data = validated_data.pop('bank')

        user = User.objects.create(username=validated_data['username'])
        user.save()
        validated_data['user'] = user

        if 'id' in bank_data:
            #update bank info
            try:
                bank_info = Bank.objects.get(pk=bank_data['id'])
                bank_info.account = bank_data['account']
                bank_info.save()
                validated_data['bank'] = bank_info
            except Bank.DoesNotExist:
                #initial data
                b = Bank.objects.create(**bank_data)
                validated_data['bank'] = b
        else:
            b = Bank.objects.create(**bank_data)
            validated_data['bank'] = b


        member = Member.objects.create(**validated_data)
        return member

    def validate(self, data):
        request = self.context['request']

        if request.method == 'POST':
            if 'username' in data:
                if Agent.objects.filter(username=data['username']).count():
                    raise serializers.ValidationError({"detail": "Username already exists"})
        return data
