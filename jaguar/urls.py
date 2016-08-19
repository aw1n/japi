"""jaguar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from rest_framework import routers

from account import views as account
from level import views as level
from bank import views as bank
from configsettings import views as settings
from tracker import views as tracker
from provider import views as provider
from transaction import views as transactions
from notifysvc import views as notifysvc

router = routers.DefaultRouter()
router.register(r'agent', account.AgentViewSet, 'agent')
router.register(r'agentapplication', account.AgentApplicationViewSet, 'agentapplication')
router.register(r'member', account.MemberViewSet, 'member')
router.register(r'memberapplication', account.MemberApplicationViewSet, 'memberapplication')
router.register(r'guest/member', account.MemberGuestViewSet, 'memberguest')
router.register(r'level', level.LevelViewSet, base_name='level')
router.register(r'bank', bank.BankViewSet, base_name='bank')
router.register(r'bankinfo', bank.BankInfoViewSet, base_name='bankinfo')
router.register(r'agentlevel', account.AgentLevelViewSet, base_name='agentlevel')
router.register(r'discount', settings.DiscountViewSet, base_name='discount')
router.register(r'returnsetting', settings.ReturnSettingsViewSet, base_name='returnsettings')
router.register(r'provider', provider.ProviderViewSet, base_name='provider')
router.register(r'commissionsetting', settings.CommissionSettingsViewSet, base_name='commissionsettings')
router.register(r'tracker', tracker.LoggingViewSet, base_name='tracker')
router.register(r'remitpayee', transactions.RemitPayeeViewSet, base_name='remitpayee')
router.register(r'onlinepayee', transactions.OnlinePayeeViewSet, base_name='onlinepayee')
router.register(r'remitinfo', transactions.RemitInfoViewSet, base_name='remitinfo')
router.register(r'transaction', transactions.TransactionViewSet, base_name='transaction')
router.register(r'onlinepayment', transactions.OnlinePaymentViewSet, base_name='onlinepayment')
router.register(r'paymenttype', transactions.PaymentTypeViewSet, base_name='paymenttype')
router.register(r'notifysvc', notifysvc.NotifySvcView, base_name='notifysvc')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
