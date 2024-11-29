from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class DataModel(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_('Nomi'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Tavsif/Izoh'))


class DataClass(BaseModel):
    data_model = models.ForeignKey(DataModel, on_delete=models.CASCADE, related_name='classes', verbose_name=_('Model'))
    title = models.CharField(max_length=250, verbose_name=_('Nomi'), unique=True)
    label = models.CharField(max_length=250, verbose_name=_('Label'), unique=True)
    description = models.TextField(blank=True, null=True, verbose_name=_('Tavsif/Izoh'))


