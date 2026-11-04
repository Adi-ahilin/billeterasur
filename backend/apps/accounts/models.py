from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.core.models import BaseModel

from .managers import UserManager
from .validators import phone_validator, validate_rut


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Persona usuaria de BilleteraSur. Inicia sesión con su correo."""

    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=10, unique=True, validators=[validate_rut])
    phone = models.CharField(max_length=12, unique=True, validators=[phone_validator])
    full_name = models.CharField(max_length=150)

    # La cuenta no se activa hasta verificar correo y teléfono (RF-01).
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["rut", "phone", "full_name"]

    def clean(self):
        super().clean()
        self.email = self.email.lower()

    def __str__(self):
        return self.email