from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource

from ui.models import Record


class RecordResource(ModelResource):
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'
        authentication = BasicAuthentication()
