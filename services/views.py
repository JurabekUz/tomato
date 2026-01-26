import cv2
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from model.models import DataModel
from base.models import DiseaseType, DiseaseLevel
from utils.exceptions import CommonException
from utils.pagination import CommonPagination
from .serializers import PredictListSerializer, PredictRetrieveSerializer, PredictSerializer, PredictResponseSerializer
import numpy as np

from .models import Predict, PredictImages
from .prediction_service import PredictionService


class DataModelSelectView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(name='disease_type', required=False, type=int)
        ]
    )
    def get(self, request, *args, **kwargs):
        disease_type = request.query_params.get('disease_type')
        if disease_type and disease_type.isdigit():
            queryset = DataModel.objects.filter(
                is_active=True, disease_type=int(disease_type)
            ).values('id', 'title')
        else:
            queryset = DataModel.objects.filter(
                is_active=True
            ).values('id', 'title')
        return Response(data=queryset)


class PredictView(APIView):

    @extend_schema(
        request=PredictSerializer,
        responses={
            status.HTTP_200_OK: PredictResponseSerializer,
            status.HTTP_400_BAD_REQUEST: None
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = PredictSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            # data_model = DataModel.objects.get(id=data['data_model'])
            data_model = DataModel.objects.filter(code__iexact='cnn').first()
            images = self.request.FILES.getlist('images')
        except:
            raise CommonException(_("Nazarda tutilmagan xatolik yuz berdi."))

        prediction_service = PredictionService()
        data_class, confidence = prediction_service.predict(images, data_model)

        predict = Predict.objects.create(
            user=request.user, 
            result=data_class, 
            data_model=data_model, 
            percentage=int(confidence * 100)
        )
        image_objs = [PredictImages(predict=predict, image=image) for image in images]
        PredictImages.objects.bulk_create(image_objs)
        return Response({'class_label': data_class.title, 'confidence': confidence}, status=status.HTTP_200_OK)


class UserPredictsListView(ListAPIView):
    queryset = Predict.objects.all()
    serializer_class = PredictListSerializer
    pagination_class = CommonPagination

    def get_queryset(self):
        # Filter predicts by the current user
        return Predict.objects.filter(user=self.request.user).select_related('result__type', 'data_model')


class UserPredictsRetrieveView(RetrieveAPIView):
    queryset = Predict.objects.all()
    serializer_class = PredictRetrieveSerializer

    def get_queryset(self):
        # Filter predicts by the current user
        return Predict.objects.filter(
            user=self.request.user
        ).select_related('result__type', 'data_model').prefetch_related('images')
