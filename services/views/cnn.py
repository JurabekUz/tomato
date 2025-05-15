from operator import index

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from model.models import DataModel, DataClass
from utils.exceptions import CommonException
from services.models import Predict, PredictImages

import numpy as np
from PIL import Image

# Load your pre-trained model_data once at the start
import tensorflow as tf

from services.serializers import PredictRetrieveSerializer

# Maxsus qatlamni ro'yxatdan o'tkazish
model = tf.keras.models.load_model(
    'model/model_data/model_CNN.h5'
)


class ImageClassificationView(APIView):
    def post(self, request, *args, **kwargs):
        data_model = DataModel.objects.filter(is_active=True).first()
        if not data_model:
            return Response({'error': 'Data model not found'}, status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('image')
        data_class = self.predict(images, data_model)

        # DBga saqlash
        predict = Predict.objects.create(user=request.user, result=None)  # To'ldiriladi
        image_objs = [PredictImages(predict=predict, image=image) for image in images]
        PredictImages.objects.bulk_create(image_objs)
        predict.result = data_class
        predict.save()
        serializer = PredictRetrieveSerializer(predict)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def predict(self, images, data_model):
        predictions = []
        for image in images:
            nm_image = self.prepare_image(image)
            predictions.append(self._predict_image(nm_image))

        print(predictions)
        max_label_index = max(predictions)
        print(max_label_index)
        class_label = DataClass.objects.filter(data_model=data_model, is_active=True).get(index=max_label_index)
        print(class_label)
        return class_label

    def prepare_image(self, image):
        image = Image.open(image)
        image = image.resize((256, 256))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image /= 255.0
        return image

    def _predict_image(self, image):
        predictions = model.predict(image)
        print(predictions)
        class_index = np.argmax(predictions, axis=1)[0]
        print("class label: ", class_index)
        return class_index
