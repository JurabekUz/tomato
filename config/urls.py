from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from config.settings import SHOW_SWAGGER
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('users.urls')),
    path('api/', include('services.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if SHOW_SWAGGER:
    urlpatterns += [
        path('api/schema', SpectacularAPIView.as_view(), name='schema'),
        path('api/swagger', SpectacularSwaggerView.as_view(), name='swagger'),
        path('api/redoc', SpectacularRedocView.as_view(), name='redoc'),
    ]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)