from django.contrib import admin
from django.contrib.auth.models import User, Group
from provider.models import Provider


# Register your models here.
admin.site.register(Provider)
admin.site.unregister(User)
admin.site.unregister(Group)
