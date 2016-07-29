import datetime
from ipware.ip import get_ip
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from account.models import (Agent, Member, AgentLevel)
from bank.models import Bank, BankInfo
from bank.serializers import BankSerializer, BankInfoSerializer
from level.serializers import SimpleLevelSerializer
from level.models import Level
from configsettings.serializers import CommissionSettingsSerializer
from configsettings.models import CommissionSettings, ReturnSettings
from jaguar.lib.optionfieldsfilter import OptionFieldsFilter
from jaguar.lib.validators import RequiredFieldValidator


class BankValidator(object):

    @staticmethod
    def validate(data):
        if data.get('id'):
            b = BankInfo.objects.get(pk=data['id'])
            for key, val in data.items():
                setattr(b, key, data[key])
            b.save()
        else:
            b = BankInfo.objects.create(**data)
        return b


class AgentLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentLevel


class AgentSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    bank = BankInfoSerializer(required=False)
    user = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())
    level = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=AgentLevel.objects.all())
    parent_agent = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Agent.objects.all())
    default_member_lv = serializers.PrimaryKeyRelatedField(required=False, queryset=Level.objects.all())
    default_return_settings = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=ReturnSettings.objects.all())
    commission_settings = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=CommissionSettings.objects.all())

    class Meta:
        model = Agent

    def create(self, validated_data):
        bank_data = validated_data.pop('bank', None)
        if bank_data:
            validated_data['bank'] = BankValidator.validate(bank_data)

        agent = Agent.objects.create(**validated_data)
        if agent:
            user = User.objects.create(username=validated_data['username'])
            agent.user = user
        return agent

    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        
        bank_data = validated_data.pop('bank', None)
        if bank_data:
            BankValidator.validate(bank_data)

        for key, val in validated_data.items():
            setattr(instance, key, validated_data[key])
        instance.save()

        return instance

    def validate(self, data):
        request = self.context['request']

        if request.method == 'POST':
            if data.get('username'):
                if Agent.objects.filter(username=data['username']).count():
                    raise serializers.ValidationError({'detail': 'Username already exists'})

            agent_level = data['level']
            if agent_level.id == 1:
                if 'parent_agent' in data and data['parent_agent']:
                    raise serializers.ValidationError({'detail': 'Parent agent is not needed in creating Level 1 Agent.'})

            if agent_level.id != 1:
                if data['parent_agent'] == None:
                    raise serializers.ValidationError({'detail': 'Parent ID is required.'})
                else:
                    p_agent = Agent.objects.get(pk=data['parent_agent'].id)
                    if int(p_agent.level.id) >= data['level']:
                        raise serializers.ValidationError({'detail': 'You({0}) are only allowed to create a level {1} agent'.format(p_agent.level, data.get('level'))})
            
        return data

    def to_representation(self, instance):
        request = self.context['request']
        ret = super(AgentSerializer, self).to_representation(instance)

        #remove other fields that are not needed in the response
        ret.pop('user', None)
        ret.pop('created_at', None)
        ret.pop('updated_at', None)
        ret.pop('updated_by', None)
        ret.pop('referring_url', None)
        ret.pop('initiated_by', None)

        # if opt_expand if provided(whatever value) we need to display more detail of some fields
        if request.GET.get('opt_expand'):
            if instance.level:
                ret['level'] = {
                    'id': instance.level.id, 
                    'name': instance.level.name
                }

            if instance.default_member_lv:
                ret['default_member_lv'] = {
                    'id': instance.default_member_lv.id, 
                    'name': instance.default_member_lv.name
                }

            if instance.parent_agent:
                ret['parent_agent'] = {
                    'id': instance.parent_agent.id, 
                    'name': instance.parent_agent.username
                }
                
            if instance.commission_settings:
                ret['commission_settings'] = {
                    'id': instance.commission_settings.id, 
                    'name': instance.commission_settings.name
                }

            if instance.default_return_settings:
                ret['default_return_settings'] = {
                    'id': instance.default_return_settings.id, 
                    'name': instance.default_return_settings.name
                }

        return ret


class AgentApplicationSerializer(AgentSerializer):
    class Meta:
        model = Agent

    def validate(self,data):
        request = self.context['request']

        if request.method == 'POST':
            data['status'] = 3
            RequiredFieldValidator.validate(data, ('username', 'phone', 'email', 'qq', 'bank'))
        return data


class MemberSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    bank = BankInfoSerializer(required=False)
    user = serializers.PrimaryKeyRelatedField(required=False,queryset=User.objects.all())
    agent = serializers.PrimaryKeyRelatedField(required=False,queryset=Agent.objects.all())

    class Meta:
        model = Member

    def create(self, validated_data):
        bank_data = validated_data.pop('bank', None)

        if bank_data:
            validated_data['bank'] = BankValidator.validate(bank_data)

        member = Member.objects.create(**validated_data)
        if member:
            user = User.objects.create(username=validated_data['username'])
            member.user = user
        return member

    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        
        bank_data = validated_data.pop('bank', None)
        if bank_data:
            BankValidator.validate(bank_data)

        for key, val in validated_data.items():
            setattr(instance, key, validated_data[key])
        instance.save()

        return instance

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if 'username' in data:
                if Agent.objects.filter(username=data['username']).count():
                    raise serializers.ValidationError({'detail': 'Username already exists'})

            parent_agent = data.get('agent')
            if parent_agent:
                try:
                    data['level'] = parent_agent.default_member_lv
                except IntegrityError, e:
                    raise serializers.ValidationError({'detail': '{0}'.format(e)})

                try:
                    data['return_settings'] = parent_agent.default_return_settings
                except IntegrityError, e:
                    raise serializers.ValidationError({'detail': '{0}'.format(e)})

            else:
                raise serializers.ValidationError({'detail': 'Parent Agent is required.'})
        return data

    def to_representation(self, instance):
        request = self.context['request']
        ret = super(MemberSerializer, self).to_representation(instance)

        #remove other fields that are not needed in the response
        ret.pop('user', None)
        ret.pop('created_at', None)
        ret.pop('updated_at', None)
        ret.pop('updated_by', None)
        ret.pop('referring_url', None)
        ret.pop('initiated_by', None)

        # if opt_expand if provided(whatever value) we need to display more detail of some fields
        if request.GET.get('opt_expand'):
            if instance.level:
                ret['level'] = {
                    'id': instance.level.id, 
                    'name': instance.level.name
                }

            if instance.parent_agent:
                ret['parent_agent'] = {
                    'id': instance.parent_agent.id, 
                    'name': instance.parent_agent.username
                }
                
            if instance.commission_settings:
                ret['commission_settings'] = {
                    'id': instance.commission_settings.id, 
                    'name': instance.commission_settings.name
                }

            if instance.default_return_settings:
                ret['default_return_settings'] = {
                    'id': instance.default_return_settings.id, 
                    'name': instance.default_return_settings.name
                }

        return ret


class MemberApplicationSerializer(MemberSerializer):
    class Meta:
        model = Member

    def validate(self,data):
        request = self.context['request']

        if request.method == 'POST':
            RequiredFieldValidator.validate(data, ('username', 'phone'))
            data['status'] = 3
        return data


class MemberGuestSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(required=False,queryset=User.objects.all())

    class Meta:
        model = Member
        fields = ('id', 'username', 'phone', 'status', 'level_lock', 'ip', 'ip', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        phone = validated_data.get('phone')

        try:
            validated_data['username'] = 'guest_{0}'.format(phone)
            validated_data['ip'] = get_ip(request)
            validated_data['status'] = 3 #pending
            member = Member.objects.create(**validated_data)
            if member:
                user = User.objects.create(username=validated_data['username'])
                member.user = user
        except IntegrityError, e:
            raise serializers.ValidationError({'detail': 'Phone number {0} already used. Please try another phone number.'.format(phone)})
        except Exception, e:
            raise serializers.ValidationError({'detail': '{0}'.format(e)})
        return member
