from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from model.models import DataModel
from .serializers import ImageUploadSerializer, PredictListSerializer, PredictRetrieveSerializer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import io

from .models import Predict, PredictImages

# Load your pre-trained model_files once at the start
model = load_model('model_files/training_model.h5')


class ImageClassificationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            images = request.FILES.getlist('image')
            class_label = self.predict(images)
            # dbga saqlash
            label_obj = DataModel.objects.filter(is_active=True).first().classes.get(class_label)
            predict = Predict.objects.create(user=request.user, result=label_obj)
            image_objs = [PredictImages(predict=predict, image=image) for image in images]
            PredictImages.objects.bulk_create(image_objs)
            return Response({'class_label': class_label}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def predict(self, images):
        class_labels = []
        for image in images:
            nm_image = self.prepare_image(image)
            class_labels.append(self.predict_image(nm_image))
        max_label = max(class_labels)
        return max_label

    def prepare_image(self, image):
        # Convert image to array and preprocess as needed
        image = Image.open(image)
        image = image.resize((224, 224))  # Adjust size as per your model_files's requirements
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image /= 255.0  # Normalize if your model_files was trained with normalized images
        return image

    def predict_image(self, image):
        # Predict the class of the image using the loaded model_files
        predictions = model.predict(image)
        class_label = np.argmax(predictions, axis=1)[0]  # Adjust based on your model_files's output
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


