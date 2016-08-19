from django.contrib import admin

from .models import PaymentType

class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

admin.site.register(PaymentType, PaymentTypeAdmin)
