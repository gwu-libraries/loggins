from tastypie.admin import ApiKeyInline

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ui import models


class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]
admin.site.unregister(User)
admin.site.register(User, UserModelAdmin)


class BuildingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(models.Building, BuildingAdmin)


class FloorAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor', 'building']
    list_filter = ['building__name']
    ordering = ['building__name', 'floor']
admin.site.register(models.Floor, FloorAdmin)


class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'floor', 'display_order']
    list_editable = ['name', 'floor', 'display_order']
admin.site.register(models.Zone, ZoneAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'building', 'floor', 'zone', 'station_name',
                    'hostname', 'ip_address', 'os', 'state',
                    'observation_time']
    list_filter = ['building']
    search_fields = ['station_name']
admin.site.register(models.Location, LocationAdmin)


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
    list_display = ['id', 'location', 'session_type', 'timestamp_start',
                    'timestamp_end']
    list_filter = [DurationFilter]
    search_fields = ['location']
admin.site.register(models.Session, SessionAdmin)
