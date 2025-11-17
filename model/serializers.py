from rest_framework.fields import ImageField, CharField, IntegerField
from rest_framework.serializers import Serializer


class ImageUploadSerializer(Serializer):
    image = ImageField()


class ResultSerializer(Serializer):
    type_title = CharField(read_only=True, source='type.title')
    title = CharField(read_only=True)
    description = CharField(read_only=True)


class DataModelSerializer(Serializer):
    id = IntegerField()
    title = CharField(read_only=True)
