from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',

    url(r'^$',
        frontpage,
        name='frontpage'),

    url(r'^battle/(?P<battle_id>\d+)/wait-on-player/$',
        wait_on_player,
        name='wait-on-player'),

    url(r'^battle/(?P<battle_id>\d+)/pick-sounds/$',
        pick_sounds,
        name='pick-sounds'),
        
    url(r'^battle/(?P<battle_id>\d+)/$',
        battle,
        name='battle'),

#    url(r'^battle/$',
#        battle,
#        name='battle'),
#
#    url(r'^compute/(?P<id1>\d+)/(?P<id2>\d+)/(?P<preset>\w+)/$',
#        compute,
#        name='compute'),
#
#    url(r'^delete_users/$',
#        delete_users,
#        name='delete-users'),

)
