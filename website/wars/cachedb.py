#from django.core.cache import cache
#
#def add_user(nickname):
#    '''Add nickname to the cache'''
#    nicknames = cache.get('nicknames')
#    if nicknames:
#        nicknames = nicknames.append(nickname)
#        cache.set('nicknames', nicknames, 60*60*24)
#    else:
#        cache.set('nicknames', [nickname], 60*60*24)
#
#def del_user(nickname):
#    '''Add nickname to the cache'''
#    nicknames = cache.get('nicknames')
#    if nicknames:
#        set_nicknames = set(nicknames)
#        set_nicknames.remove(nickname)
#        cache.set('nicknames', list(set_nicknames), 60*60*24)
#
#def user_exists_p(nickname):
#    '''Check if the nickname is present in the cache'''
#    nicknames = cache.get('nicknames')
#    if nicknames:
#        return nickname in nicknames
#    else:
#        return False
#
#def set_user_sounds(nickname, sounds):
#    cache.set('nickname_sounds_%s' % nickname, sounds, 60*60*24)
#
#def get_user_sounds(nickname):
#    sounds = cache.get('nickname_sounds_%s' % nickname)
#    return sounds if sounds else []
#
#def set_player(player, nickname):
#    cache.set('player%s' % player, nickname, 60*60*24)
#
#def player_present(player):
#    return (True if cache.get('player%s' % player) else False)
