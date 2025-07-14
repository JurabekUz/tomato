from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from model.models import DataModel, DataClass
from utils.pagination import CommonPagination
from .serializers import PredictListSerializer, PredictRetrieveSerializer
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

from .models import Predict, PredictImages

# Load your pre-trained model_data once at the start
model = tf.keras.models.load_model(
    'model_data/model_CNN.h5',
    # custom_objects={'KerasLayer': hub.KerasLayer}
)


class CNNPredictView(APIView):
    def post(self, request, *args, **kwargs):
        data_model = DataModel.objects.get(code='cnn')

        images = request.FILES.getlist('image')
        data_class = self.predict(images, data_model)

        predict = Predict.objects.create(user=request.user, result=data_class)
        image_objs = [PredictImages(predict=predict, image=image) for image in images]
        PredictImages.objects.bulk_create(image_objs)
        return Response({'class_label': data_class.title}, status=status.HTTP_200_OK)

    def predict(self, images, data_model):
        from collections import Counter
        predictions = []
        for image in images:
            nm_image = self.prepare_image(image)
            predictions.append(self._predict_image(nm_image))
        most_common = Counter(predictions).most_common(1)[0][0]

        try:
            data_class = DataClass.objects.filter(
                data_model=data_model, is_active=True
            ).get(index=most_common)
        except DataClass.DoesNotExist:
            return Response({'error': 'Label not found in DataClass'},
                            status.HTTP_404_NOT_FOUND)

        return data_class

    def prepare_image(self, image):
        # Convert image to array and preprocess as needed
        image = Image.open(image)
        image = image.resize((256, 256))  # Adjust size as per your model_data's requirements
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
    pagination_class = CommonPagination

    def get_queryset(self):
        # Filter predicts by the current user
        return Predict.objects.filter(user=self.request.user).select_related('result')


class UserPredictsRetrieveView(RetrieveAPIView):
    queryset = Predict.objects.all()
    serializer_class = PredictRetrieveSerializer

    def get_queryset(self):
        # Filter predicts by the current user
        return Predict.objects.filter(user=self.request.user).select_related('result').prefetch_related('images')


