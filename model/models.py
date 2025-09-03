from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class DataModel(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_('Nomi'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Tavsif/Izoh'))
    code = models.CharField(max_length=10, unique=True)
    file = models.FileField(upload_to='models/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Modellar")
        verbose_name = _("Model")


class DataClass(BaseModel):
    data_model = models.ForeignKey(DataModel, on_delete=models.CASCADE, related_name='classes', verbose_name=_('Model'))
    title = models.CharField(max_length=250, verbose_name=_('Nomi'))
    index = models.PositiveIntegerField(verbose_name=_('Index'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Tavsif/Izoh'))

    class Meta:
        unique_together = ('data_model', 'index')
        verbose_name = _("Model klassi")
        verbose_name_plural = _("Model klasslari")


