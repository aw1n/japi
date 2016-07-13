from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from provider import views

urlpatterns = [
    url(r'^level/$', views.LevelViewSet),
]

urlpatterns = format_suffix_patterns(urlpatterns)
