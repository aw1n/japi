from django.contrib.auth.models import User
import django_filters
from django_filters import filters
from account.models import Agent, Member

class AgentFilter(django_filters.FilterSet):
    username_q = django_filters.CharFilter(name='username', lookup_type='contains')
    real_name_q = django_filters.CharFilter(name='real_name', lookup_type='contains')
    phone_q = django_filters.CharFilter(name='phone', lookup_type='contains')
    email_q = django_filters.CharFilter(name='email', lookup_type='contains')
    wechat_q = django_filters.CharFilter(name='wechat', lookup_type='contains')
    qq_q = django_filters.CharFilter(name='qq', lookup_type='contains')
    qq_q = django_filters.CharFilter(name='qq', lookup_type='contains')
    bank_name = django_filters.CharFilter(name='bank__bank_name', lookup_type='exact')
    bank_name_q = django_filters.CharFilter(name='bank__bank_name', lookup_type='contains')
    bank_account = django_filters.CharFilter(name='bank__account', lookup_type='exact')
    bank_account_q = django_filters.CharFilter(name='bank__account', lookup_type='contains')
    return_settings = django_filters.NumberFilter(name='default_return_settings', lookup_type='exact')
    register_at = django_filters.DateFromToRangeFilter()
    commission_settings = django_filters.NumberFilter(name='commission_settings', lookup_type='exact')

    class Meta:
        model = Agent

class MemberFilter(django_filters.FilterSet):
    username_q = django_filters.CharFilter(name='username', lookup_type='contains')
    real_name_q = django_filters.CharFilter(name='real_name', lookup_type='contains')
    phone_q = django_filters.CharFilter(name='phone', lookup_type='contains')
    email_q = django_filters.CharFilter(name='email', lookup_type='contains')
    wechat_q = django_filters.CharFilter(name='wechat', lookup_type='contains')
    qq_q = django_filters.CharFilter(name='qq', lookup_type='contains')
    qq_q = django_filters.CharFilter(name='qq', lookup_type='contains')
    bank_name = django_filters.CharFilter(name='bank__bank_name', lookup_type='exact')
    bank_name_q = django_filters.CharFilter(name='bank__bank_name', lookup_type='contains')
    bank_account = django_filters.CharFilter(name='bank__account', lookup_type='exact')
    bank_account_q = django_filters.CharFilter(name='bank__account', lookup_type='contains')
    return_settings = django_filters.NumberFilter(name='return_settings', lookup_type='exact')
    register_at = django_filters.DateFromToRangeFilter()
    commission_setting = django_filters.NumberFilter(name='agent__commission_settings_id', lookup_type='exact')

    class Meta:
        model = Member