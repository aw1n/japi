from django.contrib import admin
from .models import AgentLevel

class AgentLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')

admin.site.register(AgentLevel, AgentLevelAdmin)
