from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',

    url(r'^$',
        pick_name,
        name='pick-name'),

    url(r'^sounds/$',
        pick_sounds,
        name='pick-sounds'),

    url(r'^queue/$',
        waiting_queue,
        name='queue'),

    url(r'^battle/$',
        battle,
        name='battle'),

    url(r'^compute/(?P<id1>\d+)/(?P<id2>\d+)/(?P<preset>\w+)/$',
        compute,
        name='compute'),

    url(r'^delete_users/$',
        delete_users,
        name='delete-users'),

)
