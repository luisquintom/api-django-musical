# musica/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, CancionViewSet

# El Router crea las URLs automáticamente
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'canciones', CancionViewSet, basename='canciones')

urlpatterns = [
    path('', include(router.urls)),
]