import cv2
import numpy as np
import tensorflow as tf
from collections import Counter
from django.utils.translation import gettext_lazy as _
from base.models import DiseaseLevel
from utils.exceptions import CommonException

# Fraktal o'lchamini hisoblash uchun yordamchi funksiya
def box_count(img):
    height, width = img.shape
    box_sizes = [2 ** i for i in range(1, int(np.log2(min(height, width))) + 1)]
    counts = []
    for box_size in box_sizes:
        count = 0
        for i in range(0, height, box_size):
            for j in range(0, width, box_size):
                if np.any(img[i:i + box_size, j:j + box_size]):
                    count += 1
        counts.append(count)
    counts = [c for c in counts if c > 0]
    if len(counts) < 2:
        return None
    log_sizes = np.log(box_sizes[:len(counts)])
    log_counts = np.log(counts)
    coeffs = np.polyfit(log_sizes, log_counts, 1)
    return coeffs[0]

class PredictionService:
    def predict(self, images, data_model):
        try:
            # Modelni dinamik ravishda DataModel.file manzilidan yuklash
            model_file_path = data_model.file.path
            model = tf.keras.models.load_model(model_file_path)
            print("MODEL KUTAYOTGAN SHAKL:", model.input_shape)
            print(model_file_path)
        except (IOError, ValueError) as e:
            raise CommonException(_(f"Modelni yuklashda xatolik yuz berdi: {e}"))

        predictions = []
        confidences = []
        for image in images:
            # Rasmdan xususiyatlarni olamiz
            features = self._get_features_from_image(image)
            if features is None:
                raise CommonException(
                    _("Rasm bilan ishlashda xatolik, iltimos yaxshiroq formatdagi rasm yuboring"))
            
            class_label, confidence = self._predict_image(features, model)
            predictions.append(class_label)
            confidences.append(confidence)

        try:
            most_common = Counter(predictions).most_common(1)[0][0]
            # Calculate average confidence for the most common class
            relevant_confidences = [conf for pred, conf in zip(predictions, confidences) if pred == most_common]
            avg_confidence = sum(relevant_confidences) / len(relevant_confidences)
        except IndexError:
            raise CommonException(_("Rasm kasalligi topilmadi, Uzr so'raymiz"))
        except:
            raise CommonException(_("Nazarda tutilmagan xatolik yuz berdi."))

        try:
            data_class = data_model.disease_type.disease_levels.get(index=most_common)
        except DiseaseLevel.DoesNotExist:
            raise CommonException(_("Label not found in Disease Level"))

        return data_class, avg_confidence

    def _get_features_from_image(self, image_file):
        """Taqdim etilgan algoritm yordamida rasmdan xususiyatlarni ajratib oladi."""
        try:
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            # Rasmni fayl sifatida o'qish
            image_stream = image_file.read()
            if hasattr(image_file, 'seek'):
                image_file.seek(0) # Reset pointer for further use

            image = np.frombuffer(image_stream, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            if image is None:
                return None

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            contrast = np.std(gray)
            # if contrast < 20:
            #     print("Past kontrast, o'tkazib yuborilmoqda.")
            #     return None

            gray = cv2.equalizeHist(gray)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                print("Konturlar topilmadi.")
                return None

            contour_areas = [cv2.contourArea(cnt) for cnt in contours]
            contour_perimeters = [cv2.arcLength(cnt, True) for cnt in contours]
            area_to_perimeter_ratios = [a / p if p != 0 else 0 for a, p in zip(contour_areas, contour_perimeters)]

            mean_area = np.mean(contour_areas)
            std_area = np.std(contour_areas)
            mean_perimeter = np.mean(contour_perimeters)
            std_perimeter = np.std(contour_perimeters)
            mean_area_to_perimeter_ratio = np.mean(area_to_perimeter_ratios)
            fractal_dim = box_count(thresh)

            if fractal_dim is None:
                print("Fraktal o'lchamini hisoblab bo'lmadi.")
                return None

            features = np.array([
                contrast,
                len(contours),
                mean_area,
                std_area,
                mean_perimeter,
                std_perimeter,
                mean_area_to_perimeter_ratio,
                abs(fractal_dim)
            ])
            return features.reshape(1, -1)
        except Exception as e:
            print(f"Xususiyatlarni ajratishda xatolik: {e}")
            return None

    def _predict_image(self, features, model):
        # 8 ta xususiyatni model kutgan shaklga o'zgartirish
        # (namunalar soni, xususiyatlar soni, balandlik, kanallar soni)
        features_reshaped = features.reshape(1, 8, 1, 1)

        predictions = model.predict(features_reshaped)
        class_label = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions)
        return class_label, confidence
