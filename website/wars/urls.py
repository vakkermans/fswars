from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',

    url(r'^$',
        frontpage,
        name='frontpage'),

    url(r'^battle/(?P<battle_id>\d+)/invite/$',
        wait_on_player,
        name='wait-on-player'),

    url(r'^battle/(?P<battle_id>\d+)/pick-sounds/$',
        pick_sounds,
        name='pick-sounds'),

    # for setting the chosen sounds.
    url(r'^battle/(?P<battle_id>\d+)/pick-sounds-helper/$',
        pick_sounds_helper,
        name='pick-sounds-helper'),



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

    # request current battle state over comet
    url(r'^battle/(?P<battle_id>\d+)/request-battle-status/$',
        request_battle_status,
        name='request-battle-status'),

    # browser 2 browser
    url(r'^battle/(?P<battle_id>\d+)/browser2browser/$',
        browser2browser,
        name='browser2browser'),

)
