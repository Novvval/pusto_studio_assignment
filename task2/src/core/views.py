from django.db.models import Prefetch
from rest_framework.views import APIView

from .models import PlayerPrize, PlayerLevel, Prize
from .service import PrizeExportService


def csv_serializer(data):
    return [
        data.player_level.player.player_id,
        data.player_level.level.title,
        data.player_level.is_completed,
        data.prize.prize.title
    ]


class ExportPrizesView(APIView):
    def get(self, request):
        iterator = PlayerPrize.objects.select_related(
            'player_level__player',
            'player_level__level',
            'prize__prize'
        ).prefetch_related(
            Prefetch('player_level', queryset=PlayerLevel.objects.select_related('player', 'level')),
            Prefetch('prize', queryset=Prize.objects.select_related('prize'))
        ).defer('received').iterator

        service = PrizeExportService()

        return service.export("prizes", iterator, csv_serializer)
