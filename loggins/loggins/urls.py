from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from ui.api import LocationResource

admin.autodiscover()

api_1 = Api(api_name='1')
api_1.register(LocationResource())

urlpatterns = patterns('',
    url(r'^api/', include(api_1.urls)), 
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ui.views',
    url(r'^$', 'home', name='home'),
# Requires the numeric segment of the location to be 3 digits:
#    url(r'^host/(?P<host_location>[a-z]\d{3})/$', 'host', name='host'),
#
# Allows the numeric portion to be any number of digits (1 or more):
    url(r'^location/(?P<bldgfloorcode>[a-z][0-9])/(?P<station>\w+)/$', 'location', name='location'),
# code should be something like 'g1' for Gelman 1st floor
    url(r'^floor/(?P<code>[a-z][0-9])/$', 'floor', name='floor'),
)
