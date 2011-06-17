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

    url(r'^battle/(?P<battle_id>\d+)/wait-on-sounds/$',
        wait_on_sounds,
        name='wait-on-sounds'),

#    url(r'^compute/(?P<id1>\d+)/(?P<id2>\d+)/(?P<preset>\w+)/$',
#        compute,
#        name='compute'),

    url(r'^battle/(?P<battle_id>\d+)/fight/(?P<id1>\d+)/(?P<id2>\d+)/(?P<preset>\w+)/$',
        fight,
        name='fight'),

    url(r'^battle/(?P<battle_id>\d+)/result/$',
        battle_result,
        name='result'),

    url(r'^battle/(?P<battle_id>\d+)/status/$',
        battle_status,
        name='status'),

)
