from rest_framework.fields import ImageField, CharField
from rest_framework.serializers import Serializer

from .models import DataClass


class ImageUploadSerializer(Serializer):
    image = ImageField()


class DataClassSerializer(Serializer):
    type_title = CharField(read_only=True, source='data_model.title')
    title = CharField(read_only=True)
    description = CharField(read_only=True)
