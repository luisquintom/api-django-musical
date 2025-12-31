# musica/serializers.py
from rest_framework import serializers
from .models import Usuario, Cancion

# Serializer para Canciones
class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = ['id', 'titulo', 'artista', 'owner']
        # 'owner' será de lectura solamente en la creación anidada, 
        # o lo gestionaremos desde la vista.
        read_only_fields = ['owner'] 

# Serializer para Usuarios
class UsuarioSerializer(serializers.ModelSerializer):
    # Incluimos las canciones del usuario en la respuesta JSON
    canciones = CancionSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'password', 'canciones']
        # Ocultamos el password para que no salga al LEER (seguridad básica)
        extra_kwargs = {'password': {'write_only': True}}