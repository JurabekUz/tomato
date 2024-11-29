from rest_framework.fields import ImageField
from rest_framework.serializers import Serializer, CharField

from .models import DataClass


class ImageUploadSerializer(Serializer):
    image = ImageField()


class DataClassSerializer(Serializer):
    title = CharField(read_only=True)
    description = CharField(read_only=True)