import uuid

from django.db import models


class BaseModel(models.Model):
    """Base de los modelos del proyecto: identificador opaco (UUID) y marcas de tiempo.

    El UUID evita identificadores secuenciales que se puedan adivinar en URLs y respuestas.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True