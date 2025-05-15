from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from model.models import DataModel, DataClass
from .serializers import PredictListSerializer, PredictRetrieveSerializer
import tensorflow as tf
import numpy as np
from PIL import Image

from .models import Predict, PredictImages

# Load your pre-trained model_data once at the start
model = tf.keras.models.load_model('model/model_data/training_model.h5')


class ImageClassificationView(APIView):
    def post(self, request, *args, **kwargs):
        data_model = DataModel.objects.filter(is_active=True).first()
        if not data_model:
            return Response({'error': 'Data model not found'}, status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('image')
        class_label = self.predict(images, data_model)

        # dbga saqlash
        try:
            label_obj = DataClass.objects.get(label=class_label)
        except DataClass.DoesNotExist:
            return Response({'error': 'Label not found in DataClass'}, status=status.HTTP_400_BAD_REQUEST)

        predict = Predict.objects.create(user=request.user, result=label_obj)
        image_objs = [PredictImages(predict=predict, image=image) for image in images]
        PredictImages.objects.bulk_create(image_objs)
        return Response({'class_label': class_label}, status=status.HTTP_200_OK)





    def predict(self, images, data_model):
        predictions = []
        class_labels = DataClass.objects.filter(
            data_model=data_model, is_active=True
        ).values_list('label', flat=True)

        for image in images:
            nm_image = self.prepare_image(image)
            predictions.append(self._predict_image(nm_image))
        max_label_index = np.argmax(predictions)
        return class_labels[max_label_index]

    def prepare_image(self, image):
        # Convert image to array and preprocess as needed
        image = Image.open(image)
        image = image.resize((224, 224))  # Adjust size as per your model_data's requirements
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image /= 255.0  # Normalize if your model_data was trained with normalized images
        return image

    def _predict_image(self, image):
        # Predict the class of the image using the loaded model_data
        predictions = model.predict(image)
        class_label = np.argmax(predictions, axis=1)[0]  # Adjust based on your model_data's output
        return class_label


class UserPredictsListView(ListAPIView):
    queryset = Predict.objects.all()
    serializer_class = PredictListSerializer

    def get_queryset(self):
        # Filter predicts by the current user
        return Predict.objects.filter(user=self.request.user).select_related('result')


class UserPredictsRetrieveView(RetrieveAPIView):
    queryset = Predict.objects.all()
    serializer_class = PredictRetrieveSerializer

    def get_queryset(self):
        # Filter predicts by the current user
        return Predict.objects.filter(user=self.request.user).select_related('result').prefetch_related('images')


