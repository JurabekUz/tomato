from calendar import day_abbr

# views.py
from django.shortcuts import render
from django.http import JsonResponse

from base.models import PlantType, DiseaseType, DiseaseLevel, ImageData
from model.models import DataModel
from services.prediction_service import PredictionService


def predict_page(request):
    return render(
        request, "index.html", {"plants": PlantType.objects.filter(is_active=True)}
    )


def predict_cotton_page(request):
    return render(
        request,
        "cotton_index.html",
        {"plants": PlantType.objects.filter(is_active=True)},
    )


def get_disease_types(request):
    plant_id = request.GET.get("plant")
    data = list(DiseaseType.objects.filter(plant_id=plant_id).values("id", "title"))
    return JsonResponse(data, safe=False)


def get_models(request):
    disease_type_id = request.GET.get("disease_type")
    data = list(
        DataModel.objects.filter(disease_type_id=disease_type_id).values("id", "title")
    )
    return JsonResponse(data, safe=False)


def predict_view(request):
    """
    Real ML prediction will be here.
    """
    if request.method == "POST":
        plant_id = request.POST.get("plant")
        disease_id = request.POST.get("disease")
        model_id = request.POST.get("model")
        image_files = request.FILES.getlist("image")

        if not all([plant_id, disease_id, model_id, image_files]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            # model_instance = DataModel.objects.get(id=model_id)
            model_instance = DataModel.objects.filter(code__iexact="cnn").first()
            prediction_service = PredictionService()
            data_class, confidence = prediction_service.predict_tomato_model(
                image_files, model_instance
            )

            # The prediction_result should contain class_label, description, and image URLs
            return JsonResponse(
                {
                    "class_label": data_class.title,
                    "description": data_class.description,
                    "confidence": float(confidence),
                }
            )

        except DataModel.DoesNotExist:
            return JsonResponse({"error": "Model not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST request required"}, status=400)
