from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',

    url(r'^$',
        pick_name,
        name='pick-name'),

    url(r'^sounds$',
        pick_sounds,
        name='pick-sounds'),

)