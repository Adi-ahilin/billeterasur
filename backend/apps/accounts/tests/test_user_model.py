from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import User
from apps.accounts.validators import phone_validator

CLAVE_DE_PRUEBA = "clave-de-prueba-no-real"


def datos(**cambios):
    base = {
        "email": "Ana@Example.com",
        "password": CLAVE_DE_PRUEBA,
        "rut": "12.345.678-5",
        "phone": "+56912345678",
        "full_name": "Ana Pérez",
    }
    base.update(cambios)
    return base


class UserModelTests(TestCase):
    def test_crea_usuario_normalizado_e_inactivo(self):
        user = User.objects.create_user(**datos())
        self.assertEqual(user.email, "ana@example.com")
        self.assertEqual(user.rut, "12345678-5")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)

    def test_guarda_la_clave_con_argon2(self):
        user = User.objects.create_user(**datos())
        self.assertTrue(user.password.startswith("argon2$"))
        self.assertNotIn(CLAVE_DE_PRUEBA, user.password)
        self.assertTrue(user.check_password(CLAVE_DE_PRUEBA))

    def test_el_identificador_es_un_uuid(self):
        user = User.objects.create_user(**datos())
        self.assertEqual(len(str(user.id)), 36)

    def test_rechaza_rut_con_digito_invalido(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(**datos(rut="12345678-9"))
        self.assertEqual(User.objects.count(), 0)

    def test_rechaza_rut_repetido_en_otro_formato(self):
        User.objects.create_user(**datos())
        with self.assertRaises(ValidationError):
            User.objects.create_user(**datos(email="otra@example.com", phone="+56987654321", rut="12345678-5"))

    def test_rechaza_correo_repetido_con_otras_mayusculas(self):
        User.objects.create_user(**datos())
        with self.assertRaises(ValidationError):
            User.objects.create_user(**datos(email="ANA@EXAMPLE.COM", rut="11111111-1", phone="+56987654321"))

    def test_rechaza_telefono_con_formato_invalido(self):
        for telefono in ("912345678", "+5691234567", "+56 9 1234 5678", "+569123456789"):
            with self.subTest(telefono=telefono):
                with self.assertRaises(ValidationError):
                    User.objects.create_user(**datos(phone=telefono))

    def test_exige_correo(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(**datos(email=""))

    def test_superusuario_queda_activo_y_con_permisos(self):
        admin = User.objects.create_superuser(**datos(email="admin@example.com", rut="11111111-1", phone="+56911111111"))
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class TelefonoValidatorTests(TestCase):
    def test_el_validador_exige_coincidencia_completa(self):
        phone_validator("+56912345678")
        for telefono in ("hola+56912345678", "+56912345678chao", "+56912345678\n", "+569123456789"):
            with self.subTest(telefono=telefono):
                with self.assertRaises(ValidationError):
                    phone_validator(telefono)