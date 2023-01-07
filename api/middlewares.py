import json
import random
import string

from django.db import transaction, IntegrityError
from django.http import JsonResponse

from api.models import Player, PlayerAccount
from api.views import AuthenticatedBaseMixin, AuthenticatedMixin
from currentmap.settings import GAMES_DICT


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            with transaction.atomic():
                if issubclass(view_func.view_class, AuthenticatedBaseMixin):
                    auth_key = request.headers.get("X-AuthKey", default="")
                    game_id = request.headers.get("X-GameId", default=None)
                    if game_id is None or int(game_id) not in GAMES_DICT:
                        return JsonResponse({"connected": False, "registered": False, 'error': "wrong_game_id"}, status=400)
                    game = GAMES_DICT[int(game_id)]
                    player: Player = Player.objects.filter(auth_key=Player.hash_auth_key(auth_key)).first()
                    if (issubclass(view_func.view_class, AuthenticatedMixin) or auth_key) and player is None:
                        return JsonResponse({"connected": False, "registered": False, 'error': "wrong_token_or_account"},
                                            status=401)
                    request.auth_key = auth_key
                    request.game = game
                    request.game_id = game_id
                    request.player = player
        except Exception as e:
            return JsonResponse({"connected": False, "registered": False, "error": str(e)}, status=400)
        return None
