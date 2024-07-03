from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_('Faol'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqti'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Oxirgi yangilangan vaqti'))

    class Meta:
        abstract = True


class BaseTitleModel(BaseModel):
    title = models.CharField(max_length=150, verbose_name=_('Nomi'))

    class Meta:
        abstract = True

    def __str__(self):
        a = _('Faol')
        if self.is_active is False:
            a = _('No faol')
        return f"{self.title} | {a}"


def image_data_path(instance, filename):
    # Generate path based on user and upload date
    path = f'{instance.level.type.tomato.title}/{instance.level.type.title}/{instance.level.title}/{filename}'
    return path


class TomatoType(BaseTitleModel):
    class Meta:
        ordering = ['-created_time']
        verbose_name = _('Pomidor turi')
        verbose_name_plural = _('Pomidor Turlari')


class DiseaseType(BaseTitleModel):
    tomato = models.ForeignKey(TomatoType, models.CASCADE, 'disease_types')

    class Meta:
        db_table = 'disease_types'
        ordering = ['-created_time']
        verbose_name = _('Kasallik turi')
        verbose_name_plural = _('Kasallik Turlari')

    def __str__(self):
        return f"{self.title} {self.tomato.title}"


class DiseaseLevel(BaseTitleModel):
    type = models.ForeignKey(DiseaseType, models.CASCADE, 'disease_levels')

    class Meta:
        db_table = 'disease_levels'
        ordering = ['-created_time']
        verbose_name = _('Kasallik darajasi')
        verbose_name_plural = _('Kasallik Darajalari')

    def __str__(self):
        return f"{self.title} {self.type.title} {self.type.tomato.title}"


class ImageData(BaseModel):
    level = models.ForeignKey(DiseaseLevel, models.CASCADE, 'images')
    source = models.ImageField(upload_to=image_data_path)

    class Meta:
        db_table = 'dataset_images'
        ordering = ['-created_time']
        verbose_name = _('Rasm')
        verbose_name_plural = _('Rasmlar')

