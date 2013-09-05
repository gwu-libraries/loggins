from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication,\
    Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from django.conf.urls import url

from ui.models import Location, Session


class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'
        authentication = MultiAuthentication(ApiKeyAuthentication(),
                                             Authentication())
        authorization = DjangoAuthorization()
        filtering = {
            'hostname': ALL,
            'state': ALL,
            'floor': ALL,
            'building': ALL_WITH_RELATIONS,
            'os': ALL_WITH_RELATIONS,
            'station_name': ALL_WITH_RELATIONS,
            'ip_address': 'exact',
            'floor': ALL_WITH_RELATIONS,
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<hostname>[\w-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


class SessionResource(ModelResource):
    class Meta:
        queryset = Session.objects.all()
        resource_name = 'session'
        authentication = MultiAuthentication(ApiKeyAuthentication(),
                                             Authentication())
        authorization = DjangoAuthorization()
        filtering = {
            'location': ALL,
            'session_type': ALL,
        }
