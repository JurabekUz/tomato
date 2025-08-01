from rest_framework.fields import CharField, ImageField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from model.serializers import DataClassSerializer
from .models import Predict


class ImageSerializer(Serializer):
    id = IntegerField(read_only=True)
    image = ImageField()


class PredictListSerializer(ModelSerializer):
    type_title = CharField(read_only=True, source='result.data_model.title')
    result_title = CharField(read_only=True, source='result.title')
    images_count = IntegerField(read_only=True)


    class Meta:
        model = Predict
        fields = ['id', 'result_title', 'type_title', 'images_count', 'created_time']


class PredictRetrieveSerializer(ModelSerializer):
    result = DataClassSerializer(read_only=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Predict
        fields = ['id', 'result', 'created_time', 'images']