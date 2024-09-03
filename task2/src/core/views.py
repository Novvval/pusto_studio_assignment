from django.http import StreamingHttpResponse
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from .models import PlayerLevel
from .serializers import PlayerLevelSerializer
from .service import PrizeExportService


class ExportPrizesView(APIView):
    def get(self, request) -> StreamingHttpResponse:
        service = PrizeExportService()

        return service.export("prizes")


class CreatePlayerLevelView(CreateAPIView):
    model = PlayerLevel
    serializer_class = PlayerLevelSerializer
