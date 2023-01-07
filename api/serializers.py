from rest_framework import serializers

from api.models import Group, Player, PlayerAccount, Map


class DisplayPlayerSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField("get_display_name")

    class Meta:
        model = Player
        fields = ["id", "display_name"]

    def get_display_name(self, obj):
        game = self.context.get("request").game_id
        accounts = {str(a.game): a.display_name for a in obj.player_accounts.all()}
        return accounts.get(str(game)) or list(accounts.values())[0]


class GroupSerializer(serializers.ModelSerializer):
    members = DisplayPlayerSerializer(many=True)
    owner = DisplayPlayerSerializer()

    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'owner']


class ShortGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class InviteSerializer(serializers.ModelSerializer):
    group = ShortGroupSerializer()
    from_player = DisplayPlayerSerializer()
    to_player = DisplayPlayerSerializer()

    class Meta:
        model = Group
        fields = ['id', 'group', 'from_player', 'to_player']


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class DisplayPlayerExtendedSerializer(DisplayPlayerSerializer):
    region = serializers.SerializerMethodField("get_region")
    club_tag = serializers.SerializerMethodField("get_club_tag")

    def __init__(self, *args, **kwargs):
        super(DisplayPlayerExtendedSerializer, self).__init__(*args, **kwargs)
        self.account = {}

    class Meta:
        model = Player
        fields = ["id", "display_name", "region", "club_tag"]

    def get_account(self, obj):
        if not self.account.get(obj.id):
            game = self.context.get("request").game_id
            accounts = {str(a.game): a for a in obj.player_accounts.all()}
            self.account[obj.id] = accounts.get(str(game)) or list(accounts.values())[0]
        return self.account[obj.id]

    def get_region(self, obj):
        return self.get_account(obj).region

    def get_club_tag(self, obj):
        return self.get_account(obj).club_tag


class PlayerSerializer(DisplayPlayerExtendedSerializer):
    current_map = MapSerializer()

    class Meta:
        model = Player
        fields = ["id", "display_name", "region", "club_tag", "current_pb", "current_map"]


class PlayerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerAccount
        fields = ['login', 'display_name', 'game', "region"]
