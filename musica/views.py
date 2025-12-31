from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Usuario, Cancion
from .serializers import UsuarioSerializer, CancionSerializer
from .spotify_client import SpotifyClient

# --- VIEWSET DE USUARIO ---

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=True, methods=['post'])
    def agregar_cancion(self, request, pk=None):
        usuario = self.get_object()
        serializer = CancionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def artistas_favoritos(self, request, pk=None):
        usuario = self.get_object()
        artistas_nombres = set(cancion.artista for cancion in usuario.canciones.all())
        client = SpotifyClient()
        data_artistas = []
        for nombre in artistas_nombres:
            info = client.obtener_info_artista(nombre)
            if info:
                data_artistas.append(info)
            else:
                data_artistas.append({"nombre": nombre, "error": "No encontrado en Spotify"})
        return Response(data_artistas)

# --- VIEWSET DE CANCIONES---
# Cambiamos GenericViewSet por ModelViewSet para que tenga lista y aparezca en el menú
class CancionViewSet(viewsets.ModelViewSet): 
    # Django sepa qué mostrar en /canciones/
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer

    @action(detail=False, methods=['get'])
    def buscar_spotify(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Falta el parámetro 'query'"}, status=400)
            
        client = SpotifyClient()
        resultado = client.buscar_cancion(query)
        return Response(resultado)