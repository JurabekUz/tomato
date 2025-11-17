from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PlantType, DiseaseType


class PlantTypeSelectView(APIView):
    def get(self, request):
        queryset = PlantType.objects.filter(is_active=True).values('id', 'title')
        return Response(data=list(queryset))


class DiseaseTypeSelectView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(name='plant_type', required=True, type=int)
        ]
    )
    def get(self, request):
        plant_type = int(request.get('plant_type'))
        queryset = DiseaseType.objects.filter(is_active=True, plant_id=plant_type).values('id', 'title')
        return Response(data=list(queryset))
