from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from tastypie.api import Api

from ui.api import LocationResource, SessionResource
from ui.models import Building

admin.autodiscover()

api_1 = Api(api_name='v1')
api_1.register(LocationResource())
api_1.register(SessionResource())

buildings = map(str, Building.objects.values_list('name', flat=True))
buildings_or = '|'.join(buildings)

urlpatterns = patterns('',
    url(r'^api/', include(api_1.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt'),
        name='robots.txt'),
)

urlpatterns += patterns('ui.views',
    url(r'^$', 'home', {'library': 'all'}, name='home'),
    # TODO: it would be nice to not hard-code library names, but
    # maybe at some future date.  Here's how it might work:
    # "or" match can be specified with r'^(?P<library>gelman|eckles|
    # vstc)/(?P<floor>[0-9])/$'
    #(?i) = case insensitive match
    # example:  gelman
    url(r'^(?P<library>(?i)(%s)?)/$' % buildings_or, 'home', name='home'),
    # example:  location/gelman/PC101   for PC101 in Gelman
    url(r'^(?P<library>(?i)(%s)?)/location/(?P<station>[0-9|a-z|A-Z]-[L|l|0-9]+)/$' % buildings_or,
        'location', name='location'),
    # example:  gelman/floor/2
    url(r'^(?P<library>(?i)(%s)?)/floor/(?P<floor_number>[0-9])/$' % buildings_or, 'floor', name='floor'),
    # all offline carrels
    url(r'^(?i)offline/$', 'offline', {'library': 'all'}, name='offline'),
    # example:  gelman/offline
    url(r'^(?P<library>(?i)(%s)?)/offline/$' % buildings_or, 'offline', name='offline'),
    # example:  gelman/sign/250
    url(r'^(?P<library>(?i)(%s)?)/sign/(?P<width>[0-9]+)/$' % buildings_or, 'home', name='sign'),
)
