from django.contrib import admin
from .models import Visitor, BannedIP, UntrackedUserAgent


class VisitorAdmin(admin.ModelAdmin):
    search_fields = ['ip_address', 'user_agent', 'url']
    list_display = ['ip_address', 'user', 'user_agent', 'url', 'page_views',
                    'last_update', 'session_start']


admin.site.register(Visitor, VisitorAdmin)
admin.site.register(BannedIP)
admin.site.register(UntrackedUserAgent)