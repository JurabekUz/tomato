from django.urls import path
from .views import ImageClassificationView, UserPredictsListView, UserPredictsRetrieveView

urlpatterns = [
    path('classify/', ImageClassificationView.as_view(), name='classify_image'),
    path('predicts/', UserPredictsListView.as_view(), name='predicts'),
    path('predicts/<int:pk>/', UserPredictsRetrieveView.as_view(), name='predicts_detail'),
]
