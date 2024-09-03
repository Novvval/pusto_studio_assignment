import csv
from _csv import Writer
from typing import Callable

from django.db.models import QuerySet
from django.http import StreamingHttpResponse


class CSVBuffer:
    def write(self, value):
        return value


class PrizeExportService:

    def export(self, filename: str, iterator: QuerySet.iterator, serializer: Callable) -> StreamingHttpResponse:
        writer = csv.writer(CSVBuffer())

        response = StreamingHttpResponse(self.write_rows(writer, iterator, serializer),
                                         content_type="text/csv")

        response['Content-Disposition'] = f"attachment; filename={filename}.csv"
        return response

    @staticmethod
    def write_rows(writer: Writer, iterator: QuerySet.iterator, serializer: Callable):

        headers = ['player_id', 'level', 'is_completed', 'prize']
        yield writer.writerow(headers)

        for data in iterator(chunk_size=1000):
            yield writer.writerow(serializer(data))
