from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ui import models


class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]
admin.site.unregister(User)
admin.site.register(User, UserModelAdmin)


class HostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
admin.site.register(models.Host, HostAdmin)


class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'event', 'timestamp']
    list_filter = ['event', 'timestamp']
    search_fields = ['host']
admin.site.register(models.Record, RecordAdmin)
