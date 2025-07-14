from django.urls import path

from services.views import CNNPredictView, UserPredictsListView, UserPredictsRetrieveView

urlpatterns = [
    path('predicts', UserPredictsListView.as_view(), name='predicts'),
    path('predicts/<int:pk>', UserPredictsRetrieveView.as_view(), name='predicts_detail'),
    path('predicts/cnn', CNNPredictView.as_view(), name='cnn'),
]
