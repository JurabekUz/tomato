from rest_framework.fields import ImageField
from rest_framework.serializers import Serializer


class ImageUploadSerializer(Serializer):
    image = ImageField()
