from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL

from ui.models import Location


class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                'hostname': ALL,
                'state': ALL,
            }
