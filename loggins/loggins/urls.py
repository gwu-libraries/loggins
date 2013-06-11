from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from ui.api import RecordResource

admin.autodiscover()

api_1 = Api(api_name='1')
api_1.register(RecordResource())

urlpatterns = patterns('',
    url(r'^api/', include(api_1.urls)), 
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('ui.views',
    url(r'^$', 'home', name='home'),
    url(r'^host/(?P<host_location>[a-z]\d{3})/$', 'host', name='host'),
    url(r'^floor/(?P<code>[a-z][0-9])/$', 'floor', name='floor'),
)
