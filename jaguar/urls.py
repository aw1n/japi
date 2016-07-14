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
from configsettings import views as settings
from tracker import views as tracker

router = routers.DefaultRouter()
router.register(r'agent', account.AgentViewSet, 'agent')
router.register(r'agentapplication', account.AgentApplicationViewSet, 'agentapplication')
router.register(r'member', account.MemberViewSet, 'member')
router.register(r'level', level.LevelViewSet, base_name='level')
router.register(r'discount', settings.DiscountViewSet, base_name='discount')
router.register(r'returnsettings', settings.ReturnSettingsViewSet, base_name='returnsettings')
router.register(r'returnrateconfig', settings.ReturnRateConfigViewSet, base_name='returnrateconfig')
router.register(r'commissionsettings', settings.CommissionSettingsViewSet, base_name='commissionsettings')
router.register(r'tracker', tracker.LoggingViewSet, base_name='tracker')
# router.register(r'memberapplication', account.MemberApplicationViewSet, 'memberapplication')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
