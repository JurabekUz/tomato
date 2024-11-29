from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from model.models import DataModel, DataClass
from .models import Predict, PredictImages

import numpy as np
from PIL import Image

# Load your pre-trained model_files once at the start
import tensorflow as tf
import tensorflow_hub as hub


# Maxsus qatlamni ro'yxatdan o'tkazish
model = tf.keras.models.load_model(
    'model/model_files/training_model.h5',
    custom_objects={'KerasLayer': hub.KerasLayer}
)

class ImageClassificationView(APIView):
    def post(self, request, *args, **kwargs):
        data_model = DataModel.objects.filter(is_active=True).first()
        if not data_model:
            return Response({'error': 'Data model not found'}, status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('image')
        class_labels = [self.predict([image], data_model) for image in images]

        # DBga saqlash
        predict = Predict.objects.create(user=request.user, result=None)  # To'ldiriladi
        image_objs = []
        for image, label in zip(images, class_labels):
            try:
                label_obj = DataClass.objects.get(label=label)
            except DataClass.DoesNotExist:
                continue
            predict.result = label_obj
            image_objs.append(PredictImages(predict=predict, image=image))
        PredictImages.objects.bulk_create(image_objs)
        predict.save()

        return Response({'class_labels': class_labels}, status=status.HTTP_200_OK)

    def predict(self, images, data_model):
        predictions = []
        for image in images:
            nm_image = self.prepare_image(image)
            predictions.append(self._predict_image(nm_image))

        max_label_index = np.argmax(predictions)
        class_labels = list(
            DataClass.objects.filter(data_model=data_model, is_active=True)
            .values_list("label", flat=True)
        )
        return class_labels[max_label_index]

    def prepare_image(self, image):
        image = Image.open(image)
        image = image.resize((224, 224))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image /= 255.0
        return image

    def _predict_image(self, image):
        predictions = model.predict(image)
        class_label = np.argmax(predictions, axis=1)[0]
        return class_label
