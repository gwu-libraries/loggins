from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from ui.api import RecordResource

admin.autodiscover()

api_1 = Api(api_name='1')
api_1.register(RecordResource())

urlpatterns = patterns('',
    url(r'^$', 'ui.views.home', name='home'),
    url(r'^api/', include(api_1.urls)), 
    url(r'^admin/', include(admin.site.urls)),
)
