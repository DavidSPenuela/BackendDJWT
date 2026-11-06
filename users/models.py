from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuario de la biblioteca: inicia sesión con email y tiene matrícula."""

    email = models.EmailField(unique=True)
    # Campo extra elegido: matrícula del lector (opcional y única).
    matricula = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text='Matrícula del estudiante o del personal de la biblioteca.',
    )

    USERNAME_FIELD = 'email'
    # "username" sigue siendo único en AbstractUser; se pide al crear superusuario
    # para evitar que dos superusuarios queden con username vacío (error de unicidad).
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
