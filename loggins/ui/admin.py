from django.contrib import admin

from ui import models


class HostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
admin.site.register(models.Host, HostAdmin)


class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'event', 'timestamp']
    list_filter = ['event', 'timestamp']
    search_fields = ['host']
admin.site.register(models.Record, RecordAdmin)
