# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import io

# Load your pre-trained model once at the start
model = load_model('model/training_model.h5')


class ImageClassificationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            images = request.FILES.getlist('image')
            class_label = self.predict(images)
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
        image = image.resize((224, 224))  # Adjust size as per your model's requirements
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image /= 255.0  # Normalize if your model was trained with normalized images
        return image

    def predict_image(self, image):
        # Predict the class of the image using the loaded model
        predictions = model.predict(image)
        class_label = np.argmax(predictions, axis=1)[0]  # Adjust based on your model's output
        return class_label


