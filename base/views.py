from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PlantType, DiseaseType


class PlantTypeSelectView(APIView):
    def get(self, request):
        queryset = PlantType.objects.filter(is_active=True).values('id', 'title')
        return Response(data=list(queryset))


class DiseaseTypeSelectView(APIView):
    def get(self, request):
        queryset = DiseaseType.objects.filter(is_active=True).values('id', 'title')
        return Response(data=list(queryset))