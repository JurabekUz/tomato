from django.contrib.auth import get_user_model
from django.db import models

from model.models import DataClass

User = get_user_model()


class Predict(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predicts')
    result = models.ForeignKey(DataClass, on_delete=models.SET_NULL, null=True, related_name='predicts')
    created_time = models.DateTimeField(auto_now_add=True)
    percentage = models.PositiveIntegerField(default=0)

    @property
    def images_count(self):
        return self.images.count()


class PredictImages(models.Model):
    predict = models.ForeignKey(Predict, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='predict_images/')
