from django.urls import path

from services.views import PredictView, UserPredictsListView, UserPredictsRetrieveView, DataModelSelectView

urlpatterns = [
    path('models/select', DataModelSelectView.as_view(), name='predicts'),
    path('predicts', UserPredictsListView.as_view(), name='predicts'),
    path('predicts/<int:pk>', UserPredictsRetrieveView.as_view(), name='predicts_detail'),
    path('predict', PredictView.as_view()),
]
