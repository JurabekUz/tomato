from django.urls import path

from .views import PlantTypeSelectView, DiseaseTypeSelectView

urlpatterns = [
    path('plant-types/select', PlantTypeSelectView.as_view()),
    path('disease-types/select', DiseaseTypeSelectView.as_view())
]