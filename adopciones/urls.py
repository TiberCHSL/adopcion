from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views
from .views import buscar_mascotas, ver_colectas, detalle_colecta, registro_usuario, LoginUsuarioView

urlpatterns = [
    path("", views.index, name="index"),
    path('mascota/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('buscar/', buscar_mascotas, name='buscar_mascotas'),
    path('ver_colectas/', ver_colectas, name='ver_colectas'),
    path('detalle_colecta/<int:colecta_id>/', detalle_colecta, name='detalle_colecta'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
