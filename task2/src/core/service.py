import _csv
import csv

from django.db.models import QuerySet, Prefetch
from django.http import StreamingHttpResponse

from core.models import PlayerPrize, PlayerLevel, Prize


def csv_serializer(data: PlayerPrize) -> list[str | bool]:
    return [
        data.player_level.player.player_id,
        data.player_level.level.title,
        data.player_level.is_completed,
        data.prize.prize.title
    ]


class CSVBuffer:
    def write(self, value):
        return value


class PrizeExportService:
    def export(self, filename: str) -> StreamingHttpResponse:
        iterator = PlayerPrize.objects.select_related(
            'player_level__player',
            'player_level__level',
            'prize__prize'
        ).prefetch_related(
            Prefetch('player_level', queryset=PlayerLevel.objects.select_related('player', 'level')),
            Prefetch('prize', queryset=Prize.objects.select_related('prize'))
        ).defer('received').iterator

        serializer = csv_serializer
        writer = csv.writer(CSVBuffer())

        response = StreamingHttpResponse(
            self.write_rows(writer, iterator, serializer), content_type="text/csv"
        )

        response['Content-Disposition'] = f"attachment; filename={filename}.csv"
        return response

    @staticmethod
    def write_rows(writer: _csv.writer, iterator: QuerySet.iterator, serializer: csv_serializer):
        headers = ['player_id', 'level', 'is_completed', 'prize']
        yield writer.writerow(headers)

        for data in iterator(chunk_size=1000):
            yield writer.writerow(serializer(data))
