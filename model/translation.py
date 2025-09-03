from modeltranslation.translator import register, TranslationOptions
from model.models import DataClass


@register(DataClass)
class BaseNameTranslationOptions(TranslationOptions):
    fields = ("title", "description")
