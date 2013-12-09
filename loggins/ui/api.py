from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication,\
    Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from django.conf.urls import url

from ui.models import Location, Session


class LocationResource(ModelResource):
    building_name = fields.CharField(attribute='building_name', readonly=True)
    floor_number = fields.IntegerField(attribute='floor_number', readonly=True)
    zone_name = fields.CharField(attribute='zone_name', readonly=True)

    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'
        authentication = MultiAuthentication(ApiKeyAuthentication(),
                                             Authentication())
        authorization = DjangoAuthorization()
        filtering = {
            'hostname': ALL,
            'state': ALL,
            'os': ALL_WITH_RELATIONS,
            'station_name': ALL_WITH_RELATIONS,
            'ip_address': 'exact',
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<hostname>.+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


class SessionResource(ModelResource):
    location = fields.ForeignKey(LocationResource, 'location')
    duration_minutes = fields.FloatField(attribute='duration_minutes',
                                         readonly=True)

    class Meta:
        queryset = Session.objects.all()
        resource_name = 'session'
        authentication = MultiAuthentication(ApiKeyAuthentication(),
                                             Authentication())
        authorization = DjangoAuthorization()
        filtering = {
            'location': ALL_WITH_RELATIONS,
            'session_type': ALL,
            'timestamp_start': ALL,
            'timestamp_end': ALL,
            'duration_minutes': ALL,
        }
