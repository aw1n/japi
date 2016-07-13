import datetime
from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from account.models import (Agent, Member, AgentApplication)
from bank.models import BankingInfo
from bank.serializers import BankSerializer
from level.models import Level
from configsettings.serializers import CommissionSettingsSerializer
from configsettings.models import CommissionSettings, ReturnSettings

class AgentRetrieveSerializer(serializers.ModelSerializer):

    bank = BankSerializer(required=False)
    commission_settings = CommissionSettingsSerializer(required=False)

    class Meta:
        model = Agent

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
    # commission_settings = CommissionSettingsSerializer(required=False)
    commission_settings = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=CommissionSettings.objects.all())
    level = serializers.IntegerField(required=True)
    # parent_agent = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Agent.objects.all())

    class Meta:
        model = Agent


    def create(self, validated_data):
        bank_data = validated_data.pop('bank')

        if 'id' in bank_data:
            #update bank info
            try:
                bank_info = BankingInfo.objects.get(pk=bank_data['id'])
                bank_info.account = bank_data['account']
                bank_info.save()
                validated_data['bank'] = bank_info
            except BankingInfo.DoesNotExist:
                #initial data
                b = BankingInfo.objects.create(**bank_data)
                validated_data['bank'] = b
        else:
            b = BankingInfo.objects.create(**bank_data)
            validated_data['bank'] = b


        agent = Agent.objects.create(**validated_data)
        return agent


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
                    print int(p_agent.level)
                    print data['level'] + 1
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
    # banking_info = serializers.PrimaryKeyRelatedField(required=False,queryset=BankingInfo.objects.all()) 
    # agent = serializers.PrimaryKeyRelatedField(required=False,queryset=Agent.objects.all())   

    class Meta:
        model = Member

    def validate(self, data):
        request = self.context['request']

        if request.method == 'POST':
            if 'username' in data:
                if Agent.objects.filter(username=data['username']).count():
                    raise serializers.ValidationError({"detail": "Username already exists"})
        return data
