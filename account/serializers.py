import datetime
from ipware.ip import get_ip
from django.contrib.auth.models import User, Group
from ast import literal_eval
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
            user = User.objects.create_user(username=validated_data['username'])
            # add group to user
            agent_grp = Group.objects.get(name='agent_grp')
            user.groups.add(agent_grp)
            agent.user = user
            agent.save()
        return agent

    def update(self, instance, validated_data):
        validated_data.pop('username', None)

        bank_data = validated_data.pop('bank', None)
        if bank_data:
            validated_data['bank'] = BankValidator.validate(bank_data)

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
            user = User.objects.create_user(username=validated_data['username'])
            # add group to user
            member_grp = Group.objects.get(name='member_grp')
            user.groups.add(member_grp)
            member.user = user
            member.save()
        return member

    def update(self, instance, validated_data):
        validated_data.pop('username', None)

        bank_data = validated_data.pop('bank', None)
        if bank_data:
            validated_data['bank'] = BankValidator.validate(bank_data)

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
        ret.pop('updated_at', None)
        ret.pop('updated_by', None)
        ret.pop('referring_url', None)
        ret.pop('initiated_by', None)
        if instance.last_login:
            ret['last_login'] = {
                                    'logindate': instance.last_login.logindate,
                                    'address': instance.last_login.address,
                                    'ipaddr': instance.last_login.ipaddr
                                }
        balance = instance.balance_member.all()
        if balance:
            ret['balance'] = balance[0].balance


        # if opt_expand is provided(whatever value) we need to display more detail of some fields
        if request.GET.get('opt_expand'):
            if instance.level:
                # ol = literal_eval(instance.level.online_limit)
                import json
                import ast
                import collections

                to_display = collections.OrderedDict()
                ol = collections.OrderedDict(ast.literal_eval(instance.level.online_limit)) if instance.level.online_limit else None
                ret['level'] = {
                    'id': instance.level.id,
                    'name': instance.level.name,
                    'online_limit': {
                        'upper': ol['upper'] if ol else '',
                        'lower': ol['lower'] if ol else ''
                    }
                }

            if instance.return_settings:
                ret['return_settings'] = {
                    'id': instance.return_settings.id,
                    'name': instance.return_settings.name
                }

            if instance.agent:
                ret['agent'] = {
                    'id': instance.agent.id,
                    'name': instance.agent.username
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


class MemberRegistrationSerializer(serializers.ModelSerializer):
    '''
    '''

    class Meta:
        model = Member


    def to_internal_value(self, data):
        ret = super(MemberRegistrationSerializer, self).to_internal_value(data)
        request = self.context['request']
        ret['password'] = request.POST.get('password')
        ret['confirmation_password'] = request.POST.get('confirmation_password')

        return ret

    def validate(self, data):
        request = self.context['request']

        validated_data = dict()
        if request.method == 'POST':
            required_fields = ('username',
                                'password',
                                'confirmation_password',
                                'real_name',
                                'withdraw_password',
                                'phone',
                                'qq')
            RequiredFieldValidator.validate(data, required_fields)

            # check if username is already in used
            user_check = User.objects.filter(username=data.get('username'))
            if user_check:
                raise serializers.ValidationError({'detail': 'Username already in use!'})
            validated_data['username'] = data.get('username')

            # check if password and confirmation password matched
            if not data.get('password') == data.get('confirmation_password'):
                raise serializers.ValidationError({'detail': 'Password did not matched!'})
            validated_data['password'] = data.get('password')
            validated_data['withdraw_password'] = data.get('withdraw_password')

            # get default agent
            agent_check = Agent.objects.get(pk=1)

            # if promo code
            # check if promo code is valid
            if data.get('promo_code', None):
                agent_check = Agent.objects.get(promo_code=data.get('promo_code'))
                if not agent_check:
                    raise serializers.ValidationError({'detail': 'Invalid Promo Code!'})
            # set member's agent to the agent with the promo code
            validated_data['agent'] = agent_check
            # set level to agent's default member level
            validated_data['level'] = agent_check.default_member_lv
            # set return settings to agent's default_return_settings
            validated_data['return_settings'] = agent_check.default_return_settings

            # real name, phone, qq
            validated_data['real_name'] = data.get('real_name')
            validated_data['phone'] = data.get('phone')
            validated_data['qq'] = data.get('qq')

            # set status to pending
            validated_data['status'] = 3

            # get/set register_ip
            ipaddr = self.__get_ip_addr(request)
            validated_data['register_ip'] = ipaddr

            # check if register ip is already used
            member_ip_check = Member.objects.filter(register_ip=ipaddr)
            if member_ip_check:
                validated_data['ip_repeated'] = True
                # update existing member ip_repeated
                for member in member_ip_check:
                    member.ip_repeated = True
                    member.save()
        return validated_data

    def __get_ip_addr(self, request):
        '''
        '''

        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ipaddr:
            # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
            ipaddr = ipaddr.split(', ')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR', '')

        return ipaddr

    def create(self, validated_data):
        '''
        '''

        password = validated_data.pop('password')
        member = Member.objects.create(**validated_data)
        if member:
            user = User.objects.create_user(username=validated_data['username'],
                                            password=password)
            # add group to user
            member_grp = Group.objects.get(name='member_grp')
            user.groups.add(member_grp)
            # Set balance to 0
            member.balance_member.create(balance=0)
            member.user = user
            member.save()
        return member
