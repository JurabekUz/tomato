# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# from model.models import DataModel, DataClass
# from services.models import Predict, PredictImages
#
# import pickle
# import joblib
# import numpy as np
# from PIL import Image
#
# # Load your pre-trained model_data once at the start
# import tensorflow as tf
# from sklearn.preprocessing import StandardScaler
#
# from services.serializers import PredictRetrieveSerializer
#
#
#
# # Pickle orqali modelni yuklash
# knn_model = joblib.load('model/model_data/knn_model_last.pkl')
# # Загрузка модели VGG16 для извлечения признаков
# base_model = tf.keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
#
# class ImageClassificationKNNView(APIView):
#     permission_classes = []
#
#     def post(self, request, *args, **kwargs):
#         data_model = DataModel.objects.filter(is_active=True).first()
#         if not data_model:
#             return Response({'error': 'Data model not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         images = request.FILES.getlist('image')
#         data_class = self.predict(images, data_model)
#
#         # DBga saqlash
#         predict = Predict.objects.create(user=request.user, result=None)  # To'ldiriladi
#         image_objs = [PredictImages(predict=predict, image=image) for image in images]
#         PredictImages.objects.bulk_create(image_objs)
#         predict.result = data_class
#         predict.save()
#         serializer = PredictRetrieveSerializer(predict)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def predict(self, images, data_model):
#         predictions = []
#         for image in images:
#             nm_image = self.prepare_image(image)
#             predictions.append(self._predict_image(nm_image))
#
#         print(predictions)
#         max_label_index = max(predictions)
#         print(max_label_index)
#         class_label = DataClass.objects.filter(data_model=data_model, is_active=True).get(index=max_label_index)
#         print(class_label)
#         return class_label
#
#     def prepare_image(self, image):
#         image = Image.open(image)
#         image = image.resize((256, 256))
#         image = tf.keras.preprocessing.image.img_to_array(image)
#         image = np.expand_dims(image, axis=0)
#         image /= 255.0
#         return image
#
#     def _predict_image(self, image):
#
#         # Извлечение признаков
#         features = base_model.predict(image)
#
#         # Преобразуем признаки в одномерный массив
#         features = features.flatten()
#
#         # Стандартизируем признаки, если использовалась стандартизация при обучении
#         scaler = StandardScaler()
#         features = scaler.fit_transform(features.reshape(-1, 1)).flatten()
#
#         # Предсказание с использованием модели KNN
#         predictions = knn_model.predict(features.reshape(1, -1))
#
#         # predictions = knn_model.predict(image)
#
#         # Bashorat ehtimolligini olish (agar qo'llab-quvvatlansa)
#         if hasattr(knn_model, 'predict_proba'):
#             probabilities = knn_model.predict_proba(image)
#             print("Ehtimollar:", probabilities)
#
#         print(predictions)
#         class_index = np.argmax(predictions, axis=1)[0]
#         print("class label: ", class_index)
#         return class_index
#
