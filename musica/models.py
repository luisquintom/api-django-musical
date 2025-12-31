# musica/models.py
from django.db import models

# Modelo de Usuario
# Django creará la tabla 'musica_usuario' automáticamente
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    # unique=True evita correos repetidos (Validación automática de base de datos)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Modelo de Canción
class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    
    # ForeignKey: Relación Uno a Muchos (Un usuario tiene muchas canciones)
    # related_name='canciones' nos permite acceder desde el usuario a sus canciones
    # on_delete=models.CASCADE significa que si borras al usuario, se borran sus canciones
    owner = models.ForeignKey(Usuario, related_name='canciones', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"