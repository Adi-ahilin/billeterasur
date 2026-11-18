from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistroSerializer, UsuarioCreadoSerializer


class RegistroView(APIView):
    """Crea una cuenta inactiva hasta verificar correo y teléfono (RF-01)."""

    permission_classes = [AllowAny]   # el resto de la API exige sesión (RS-03)
    throttle_scope = "registro"       # limita ráfagas de registro (RS-06)

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        datos = UsuarioCreadoSerializer(user).data
        datos["mensaje"] = "Cuenta creada. Verifica tu correo y tu teléfono para activarla."
        return Response(datos, status=status.HTTP_201_CREATED)