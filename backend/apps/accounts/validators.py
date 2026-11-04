import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Solo dígitos ASCII: \d aceptaría también dígitos de otros alfabetos.
_RUT_RE = re.compile(r"([0-9]{7,8})-?([0-9K])")

phone_validator = RegexValidator(
    regex=r"\A\+56[0-9]{9}\Z",
    message="Usa el formato +56912345678.",
    code="telefono_formato",
)


def rut_check_digit(body: str) -> str:
    """Calcula el dígito verificador (módulo 11) del cuerpo de un RUT."""
    total = 0
    factor = 2
    for digit in reversed(body):
        total += int(digit) * factor
        factor = 2 if factor == 7 else factor + 1
    remainder = 11 - (total % 11)
    if remainder == 11:
        return "0"
    if remainder == 10:
        return "K"
    return str(remainder)


def normalize_rut(value: str) -> str:
    """Devuelve el RUT en formato canónico (12345678-5) o lanza ValidationError."""
    cleaned = str(value).replace(".", "").replace(" ", "").upper()
    match = _RUT_RE.fullmatch(cleaned)
    if match is None:
        raise ValidationError("El RUT no tiene un formato válido.", code="rut_formato")
    body, dv = match.groups()
    return f"{body}-{dv}"


def validate_rut(value: str) -> None:
    """Rechaza un RUT con formato inválido o con dígito verificador incorrecto."""
    body, dv = normalize_rut(value).split("-")
    if rut_check_digit(body) != dv:
        raise ValidationError("El dígito verificador del RUT no es válido.", code="rut_dv")