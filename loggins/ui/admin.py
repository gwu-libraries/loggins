from django.contrib import admin

from ui import models


class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'event', 'timestamp']
    list_filter = ['event', 'timestamp']
    search_fields = ['host']
admin.site.register(models.Record, RecordAdmin)
