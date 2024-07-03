from modeltranslation.translator import register, TranslationOptions
from .models import DiseaseType, DiseaseLevel, TomatoType

models_list = [DiseaseLevel, DiseaseType, TomatoType]


@register(models_list)
class BaseNameTranslationOptions(TranslationOptions):
    fields = ("title",)
