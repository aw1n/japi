from django.contrib import admin
from .models import Bank

class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank')

    ordering = ['rank']

admin.site.register(Bank, BankAdmin)