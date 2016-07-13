from django.contrib.auth.models import User
import django_filters
from account.models import Agent, Member

class AgentFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name="username", lookup_type="contains")
    # register_at = django_filters.DateFromToRangeFilter()


    class Meta:
        model  = Agent
        fields = ['username',
                  'register_at',
                  'status',
                  'commission_settings',
                  'default_return_settings',
                  'level',
                  'parent_agent',
                  'promo_code',
                  'gender',
                  'real_name',
                  'phone',
                  'email',
                  'wechat',
                  'qq',
                  'bank',
                  'bank__account']

# class CustomerFilter(django_filters.FilterSet):
#     reseller_name = django_filters.CharFilter(name="profile__reseller_name", lookup_type="icontains")
#     company_name  = django_filters.CharFilter(name="profile__company_name", lookup_type="icontains")
#     created_by    = django_filters.CharFilter(name="profile__created_by", lookup_type="exact")
    
#     class Meta:
#         model  = User
#         fields = ['reseller_name','company_name','created_by']