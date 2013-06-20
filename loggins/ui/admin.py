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


class DurationFilter(admin.SimpleListFilter):
    title = 'duration'
    parameter_name = 'duration'

    def lookups(self, request, model_admin):
        return [('0-5', '0-5'),
                ('5-10', '5-10'),
                ('10-30', '10-30'),
                ('30-60', '30-60'),
                ('60-120', '60-120'),
                ('120+', '120+')]
        
    def queryset(self, request, queryset):
        if self.value() == '0-5':
            return queryset.filter(duration_minutes__lte=5)
        elif self.value() == '5-10':
            return queryset.filter(duration_minutes__gt=5,
                    duration_minutes__lte=10)
        elif self.value() == '10-30':
            return queryset.filter(duration_minutes__gt=10, 
                    duration_minutes__lte=30)
        elif self.value() == '30-60':
            return queryset.filter(duration_minutes__gt=30,
                    duration_minutes__lte=60)
        elif self.value() == '60-120':
            return queryset.filter(duration_minutes__gt=60,
                    duration_minutes__lte=120)
        elif self.value() == '120+':
            return queryset.filter(duration_minutes__gt=120)


class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'duration_minutes', 'duration',
            'timestamp_login', 'timestamp_logout']
    list_filter = [DurationFilter]
    search_fields = ['host']
admin.site.register(models.Session, SessionAdmin)


class AnomalyAdmin(admin.ModelAdmin):
    list_display = ['id', 'login']
admin.site.register(models.Anomaly, AnomalyAdmin)
