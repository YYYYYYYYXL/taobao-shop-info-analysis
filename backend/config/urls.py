from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from analysis.views import api_index, favicon

urlpatterns = [
    path('', api_index),
    path('favicon.ico', favicon),
    path('admin/', admin.site.urls),
    path('api/', include('analysis.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
