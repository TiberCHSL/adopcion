from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import buscar_mascotas

urlpatterns = [
    path("", views.index, name="index"),
    path('mascota/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('buscar/', buscar_mascotas, name='buscar_mascotas'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
