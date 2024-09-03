from rest_framework import serializers
from core.models import PlayerLevel, PlayerPrize


class PlayerLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerLevel
        fields = "__all__"
        read_only_fields = ['id']
