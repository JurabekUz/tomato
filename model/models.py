from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class DataModel(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_('Nomi'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Tavsif/Izoh'))
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class DataClass(BaseModel):
    data_model = models.ForeignKey(DataModel, on_delete=models.CASCADE, related_name='classes', verbose_name=_('Model'))
    title = models.CharField(max_length=250, verbose_name=_('Nomi'))
    index = models.PositiveIntegerField(verbose_name=_('Index'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Tavsif/Izoh'))

    class Meta:
        unique_together = ('data_model', 'index')


