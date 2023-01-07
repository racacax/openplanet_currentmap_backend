import datetime
import json
import random
import string

from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from api.models import Player, PlayerAccount, Group, Invite, Map
from api.serializers import GroupSerializer, InviteSerializer, PlayerSerializer, DisplayPlayerSerializer, \
    DisplayPlayerExtendedSerializer, PlayerAccountSerializer
from utils import catch_exception


class AuthenticatedBaseMixin(object):
    def __init__(self, *args, **kwargs):
        super(AuthenticatedBaseMixin, self).__init__(*args, **kwargs)
        self.auth_key = None
        self.game = None
        self.player = None


class AuthenticatedMixin(AuthenticatedBaseMixin):
    pass


class RegisterView(AuthenticatedBaseMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                if not request.auth_key:
                    request.auth_key = ''.join(
                        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
                        range(64))
                    request.player = Player.objects.create(auth_key=Player.hash_auth_key(request.auth_key))
                body: dict = json.loads(request.body)
                login = body["login"]
                name = body["name"]
                nickname = body.get("nickname", None)
                club_tag = body.get("club_tag", None)
                region = body.get("region", None)
                _, created = PlayerAccount.objects.update_or_create(player=request.player, login=login,
                                                                 game=request.game_id,
                                                                 defaults={
                                                                     "name": name,
                                                                     "club_tag": club_tag,
                                                                     "nickname": nickname,
                                                                     "region": region
                                                                 })
                if created:
                    return JsonResponse(
                        {"connected": True, "registered": True, "auth_key": request.auth_key, "error": "",
                         "accounts": PlayerAccountSerializer(request.player.player_accounts, many=True).data})

        except IntegrityError as e:
            return JsonResponse({"connected": False, "registered": False, "error": "account_exists"}, status=400)
        except Exception as e:
            return JsonResponse({"connected": False, "registered": False, "error": str(e)},
                                status=400)

        return JsonResponse({"connected": True, "registered": False, "error": "",
                             "accounts": PlayerAccountSerializer(request.player.player_accounts, many=True).data})


class GroupsOwnedView(AuthenticatedMixin, View):

    def get(self, request, *args, **kwargs):
        groups = GroupSerializer((request.player.owned_groups
                                  .select_related("owner")
                                  .prefetch_related("members__player_accounts", "owner__player_accounts")), many=True,
                                 context={'request': request})

        return JsonResponse(groups.data, safe=False)

    @catch_exception
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        group = Group.objects.create(name=data["name"], owner=request.player)
        return JsonResponse({"id": group.id})

    @catch_exception
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        return JsonResponse({"done": Group.objects.filter(id=data["id"], owner=request.player).delete()[0] > 0})


class GroupsJoinedView(AuthenticatedMixin, View):

    def get(self, request, *args, **kwargs):
        groups = GroupSerializer((request.player.joined_groups
                                  .select_related("owner")
                                  .prefetch_related("members__player_accounts", "owner__player_accounts")), many=True,
                                 context={'request': request})
        return JsonResponse(groups.data, safe=False)

    @catch_exception
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        group = Group.objects.get(id=data["id"])
        request.player.joined_groups.remove(group)
        return JsonResponse({"done": True})


class SentInvitesView(AuthenticatedMixin, View):

    def get(self, request, *args, **kwargs):
        groups = InviteSerializer(request.player.sent_invites.select_related("group"), many=True,
                                  context={'request': request})
        return JsonResponse(groups.data, safe=False)

    @catch_exception
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        group = Group.objects.get(id=data["id"])
        if group.owner_id != request.player.id:
            raise Exception("wrong_owner")
        player_id = data.get("player_id")
        if Player.objects.filter(id=player_id, joined_groups=group).exists():
            return JsonResponse({"error": "already_member"}, status=400)
        _, created = Invite.objects.get_or_create(from_player=request.player, to_player_id=player_id, group=group)
        if not created:
            return JsonResponse({"error": "invite_exists"}, status=400)
        return JsonResponse({"id": group.id})

    @catch_exception
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        invite = Invite.objects.get(id=data["id"], from_player=request.player)
        invite.delete()
        return JsonResponse({"done": True})


class ReceivedInvitesView(AuthenticatedMixin, View):

    def get(self, request, *args, **kwargs):
        groups = InviteSerializer(request.player.received_invites.select_related("group"), many=True,
                                  context={'request': request})
        return JsonResponse(groups.data, safe=False)

    @catch_exception
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        invite = Invite.objects.select_related("group").get(id=data["id"], to_player=request.player)
        invite.delete()
        request.player.joined_groups.add(invite.group.id)
        return JsonResponse({"id": invite.group.id})

    @catch_exception
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        invite = Invite.objects.get(id=data["id"], to_player=request.player)
        invite.delete()
        return JsonResponse({"done": True})


class RemovePlayerView(AuthenticatedMixin, View):

    @catch_exception
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        group = Group.objects.get(id=data["group_id"], owner=request.player)
        group.members.remove(Player(id=data["player_id"]))
        return JsonResponse({"done": True})


class LoopView(AuthenticatedMixin, View):

    @catch_exception
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        player_account = request.player.player_accounts.get(game=request.game_id)
        request.player.current_pb = data["current_pb"]
        current_map = Map.objects.filter(uid=data["map"]["uid"]).first()
        if not current_map:
            current_map = Map.objects.create(uid=data["map"]["uid"],
                                             name=data["map"]["name"],
                                             author=data["map"]["author"],
                                             author_time=data["map"]["author_time"],
                                             game=request.game_id,
                                             gold_time=data["map"]["gold_time"],
                                             silver_time=data["map"]["silver_time"],
                                             bronze_time=data["map"]["bronze_time"])
        request.player.current_map = current_map
        request.player.last_online = timezone.now()
        request.player.save()
        oldest_online = timezone.now() - timezone.timedelta(minutes=5)
        players = Player.objects.prefetch_related("player_accounts").select_related("current_map").filter(
            Q(owned_groups=Group(id=data["group_id"])) | Q(joined_groups=Group(id=data["group_id"])))\
            .exclude(current_map=None)\
            .filter(last_online__gt=oldest_online)\
            .distinct()
        return JsonResponse(PlayerSerializer(players, context={'request': request}, many=True).data, safe=False)


class FindPlayerView(AuthenticatedMixin, View):

    @catch_exception
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        return JsonResponse(DisplayPlayerExtendedSerializer(
            Player.objects.prefetch_related("player_accounts")
            .exclude(Q(joined_groups=Group(data["group_id"])) | Q(owned_groups=Group(data["group_id"])))
            .filter(
                Q(player_accounts__name__icontains=data["player_name"]) | Q(
                    player_accounts__nickname__icontains=data["player_name"]))[0:10], context={'request': request},
            many=True).data, safe=False)
