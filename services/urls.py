from django.urls import path

from services.views import PredictView, UserPredictsListView, UserPredictsRetrieveView, DataModelSelectView

urlpatterns = [
    path('models/select', DataModelSelectView.as_view(), name='predicts'),
    path('predicts', UserPredictsListView.as_view(), name='predicts'),
    path('predicts/<int:pk>', UserPredictsRetrieveView.as_view(), name='predicts_detail'),
    path('predict', PredictView.as_view()),
]


from .render_views import get_disease_types, get_models, predict_view


urlpatterns += [
    path('site/disease-types/', get_disease_types),
    path('site/models/', get_models),
    path('site/predict/', predict_view),
]

