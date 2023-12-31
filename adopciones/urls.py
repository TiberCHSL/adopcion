from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views
from .views import buscar_mascotas, ver_colectas, detalle_colecta, registro_usuario, LoginUsuarioView, perfil_usuario, agregar_datos_pago, crear_seguimiento, organizacion_index
from .views import sedes_organizacion, mascotas_sede, agregar_mascota
urlpatterns = [
    
    path("", views.index, name="index"),
    path('mascota/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('buscar/', buscar_mascotas, name='buscar_mascotas'),
    path('ver_colectas/', ver_colectas, name='ver_colectas'),
    path('detalle_colecta/<int:colecta_id>/', detalle_colecta, name='detalle_colecta'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('agregar_datos_pago/', agregar_datos_pago, name='agregar_datos_pago'),
    path('crear_seguimiento/<int:mascota_id>/', crear_seguimiento, name='crear_seguimiento'),
    path('lista_seguimientos/<int:mascota_id>/', views.lista_seguimientos, name='lista_seguimientos'),
    path('crear_vacuna/<int:mascota_id>/', views.crear_vacuna, name='crear_vacuna'),
    path('eliminar_datos_pago/', views.eliminar_datos_pago, name='eliminar_datos_pago'),
    path('lista_vacunas/<int:seguimiento_id>/', views.lista_vacunas, name='lista_vacunas'),
    path('organizacion_index/', organizacion_index, name='organizacion_index_view'),
    path('sedes_organizacion/', sedes_organizacion, name='sedes_organizacion_view'),
    path('mascotas_sede/<str:sede_id>/', mascotas_sede, name='mascotas_sede_view'),
    path('agregar_mascota/<str:sede_id>/', agregar_mascota, name='agregar_mascota_view'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
