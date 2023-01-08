from django.utils.crypto import get_random_string

from api.models import Player, PlayerAccount


def get_reset_token_from_login(login, game_id):
    player_account = PlayerAccount.objects.select_related('player').filter(login=login, game=game_id).first()
    if not player_account:
        return None
    auth_key = get_random_string(32)
    player_account.player.auth_key = player_account.player.hash_auth_key(auth_key)
    player_account.player.save()
    return auth_key
