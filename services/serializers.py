from rest_framework.fields import CharField, ImageField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from model.serializers import DataClassSerializer
from .models import Predict


class ImageSerializer(Serializer):
    id = IntegerField(read_only=True)
    image = ImageField()


class PredictListSerializer(ModelSerializer):
    result = CharField(read_only=True, source='predict.title')
    images_count = IntegerField(read_only=True, source='images_count')


    class Meta:
        model = Predict
        fields = ['id', 'result', 'images_count', 'created_time']


class PredictRetrieveSerializer(ModelSerializer):
    result = DataClassSerializer(read_only=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Predict
        fields = ['id', 'result', 'created_time', 'images']