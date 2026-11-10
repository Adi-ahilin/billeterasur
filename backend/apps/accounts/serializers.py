from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import User
from .validators import normalize_rut, phone_validator, validate_rut


class RegistroSerializer(serializers.Serializer):
    """Valida los datos de registro (RF-01). Toda la validación ocurre en el servidor (RS-04)."""

    email = serializers.EmailField()
    rut = serializers.CharField(max_length=13, help_text="12345678-5 o 12.345.678-5")
    phone = serializers.CharField(max_length=12, help_text="+56912345678")
    full_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_email(self, value):
        value = value.strip().lower()
        # Nota de seguridad: informar que el correo existe permite enumerar usuarios.
        # Se acepta en el registro por usabilidad; el login no lo hace (RF-02).
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este correo.")
        return value

    def validate_rut(self, value):
        try:
            canonico = normalize_rut(value)
            validate_rut(canonico)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        if User.objects.filter(rut=canonico).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este RUT.")
        return canonico

    def validate_phone(self, value):
        value = value.strip().replace(" ", "")
        try:
            phone_validator(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este teléfono.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        tentativo = User(
            email=attrs["email"], rut=attrs["rut"],
            phone=attrs["phone"], full_name=attrs["full_name"],
        )
        try:
            validate_password(attrs["password"], tentativo)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class UsuarioCreadoSerializer(serializers.ModelSerializer):
    """Respuesta mínima: no devuelve RUT ni teléfono (RS-11)."""

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "is_active"]