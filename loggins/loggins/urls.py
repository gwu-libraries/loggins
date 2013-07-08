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
    # example:  location/g2/PC101   for PC101 on Gelman 2nd floor
    url(r'^location/(?P<bldgfloorcode>[a-z][0-9])/(?P<station>\w+)/$',
        'location', name='location'),
    # code should be something like 'g2' for Gelman 2nd floor
    url(r'^floor/(?P<code>[a-z][0-9])/$', 'floor', name='floor'),
)
