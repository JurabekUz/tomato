from rest_framework.fields import CharField, ImageField, IntegerField, ListField
from rest_framework.serializers import ModelSerializer, Serializer, PrimaryKeyRelatedField

from model.models import DataModel
from model.serializers import DataClassSerializer
from .models import Predict



class ImageSerializer(Serializer):
    id = IntegerField(read_only=True)
    image = ImageField()


class PredictSerializer(Serializer):
    images = ListField(child=ImageField())
    data_model = PrimaryKeyRelatedField(queryset=DataModel.objects.filter(is_active=True))


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


class PredictResponseSerializer(Serializer):
    class_label = CharField(
        label="Tasniflash natijasi",
        help_text="Tahmin qilingan rasmning sinf nomi."
    )

