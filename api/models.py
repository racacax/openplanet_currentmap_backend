import hashlib

from django.db import models

# Create your models here.
from currentmap.settings import GAMES


class Map(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    game = models.IntegerField(choices=GAMES)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    author_time = models.IntegerField()
    gold_time = models.IntegerField()
    silver_time = models.IntegerField()
    bronze_time = models.IntegerField()
    trackmaster_time = models.IntegerField(null=True)


class Player(models.Model):
    auth_key = models.CharField(max_length=64, unique=True)
    current_pb = models.IntegerField(null=True)
    current_map = models.ForeignKey(Map, on_delete=models.SET_NULL, related_name="players", null=True)
    last_online = models.DateTimeField(null=True)

    @staticmethod
    def hash_auth_key(auth_key):
        return hashlib.sha256(auth_key.encode()).hexdigest()


class Group(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="owned_groups")
    members = models.ManyToManyField(Player, related_name="joined_groups", blank=True)


class Invite(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invites")
    from_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="sent_invites")
    to_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="received_invites")


class PlayerAccount(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player_accounts")
    login = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    nickname = models.CharField(max_length=128, null=True)
    club_tag = models.CharField(max_length=128, null=True)
    region = models.CharField(max_length=128, null=True)
    game = models.IntegerField(choices=GAMES)

    class Meta:
        unique_together = (("player", "game"), ("game", "login"))

    @property
    def display_name(self):
        display_name = ""
        if self.club_tag:
            display_name += f"[{self.club_tag}$fff] "
        if self.nickname:
            display_name += self.nickname
        else:
            display_name += self.name
        return display_name
