from django.contrib.auth import get_user_model
from django.db import models

from base.models import DiseaseLevel
from model.models import DataModel

User = get_user_model()


class Predict(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predicts')
    data_model = models.ForeignKey(DataModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='predicts')
    result = models.ForeignKey(DiseaseLevel, on_delete=models.SET_NULL, null=True, blank=True, related_name='predicts')
    created_time = models.DateTimeField(auto_now_add=True)
    percentage = models.PositiveIntegerField(default=0)

    @property
    def images_count(self):
        return self.images.count()


class PredictImages(models.Model):
    predict = models.ForeignKey(Predict, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='predict_images/')
