from modeltranslation.translator import register, TranslationOptions
from .models import DiseaseType, DiseaseLevel, PlantType

models_list = [DiseaseLevel, DiseaseType, PlantType]


@register(models_list)
class BaseNameTranslationOptions(TranslationOptions):
    fields = ("title",)
