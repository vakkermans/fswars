from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'frontpage.html'}, name='frontpage'),

    url(r'^wars/', include('wars.urls', namespace='wars')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % settings.STATIC_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    )
