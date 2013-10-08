from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from tastypie.api import Api

from ui.api import LocationResource, SessionResource

admin.autodiscover()

api_1 = Api(api_name='v1')
api_1.register(LocationResource())
api_1.register(SessionResource())

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
    url(r'^(?i)gelman/$', 'home', {'library': 'gelman'}, name='gelman-home'),
    url(r'^(?i)eckles/$', 'home', {'library': 'eckles'}, name='eckles-home'),
    url(r'^(?i)vstc/$', 'home', {'library': 'vstc'}, name='vstc-home'),
    # example:  location/g2/PC101   for PC101 on Gelman 2nd floor
    url(r'^location/(?P<bldgfloorcode>[a-z|A-Z][0-9])/(?P<station>[0-9|a-z|A-Z]-[L|l|0-9]+)/$',
        'location', name='location'),
    # code should be something like 'g2' for Gelman 2nd floor
    url(r'^floor/(?P<code>[a-z|A-Z][0-9])/$', 'floor', name='floor'),
    # offline carrels
    url(r'^(?i)gelman/offline$', 'offline', {'library': 'gelman'}, name='gelman-offline'),
    url(r'^(?i)eckles/offline$', 'offline', {'library': 'eckles'}, name='eckles-offline'),
    url(r'^(?i)vstc/offline$', 'offline', {'library': 'vstc'}, name='vstc-offline'),
    #    url(r'^robots.txt$', 'robots', name='robots'),
)
