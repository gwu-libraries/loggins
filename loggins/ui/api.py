from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL

from ui.models import Record


class RecordResource(ModelResource):
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                'hostname': ALL,
                'event': ALL,
                'timestamp': ALL,
            }
