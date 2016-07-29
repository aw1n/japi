from django.contrib import admin
from django.contrib.auth.models import User, Group
from provider.models import Provider

admin.site.register(Provider)
admin.site.unregister(User)
admin.site.unregister(Group)
