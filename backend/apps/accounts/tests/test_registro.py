from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User

CLAVE = "billetera-segura-2026"


def payload(**cambios):
    base = {
        "email": "Ana@Example.com", "rut": "12.345.678-5", "phone": "+56912345678",
        "full_name": "Ana Pérez", "password": CLAVE, "password2": CLAVE,
    }
    base.update(cambios)
    return base


class RegistroAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("accounts:registro")

    def test_registro_exitoso_crea_cuenta_inactiva(self):
        r = self.client.post(self.url, payload(), format="json")
        self.assertEqual(r.status_code, 201)
        user = User.objects.get()
        self.assertEqual(user.email, "ana@example.com")
        self.assertEqual(user.rut, "12345678-5")
        self.assertFalse(user.is_active)

    def test_la_respuesta_no_expone_datos_sensibles(self):
        r = self.client.post(self.url, payload(), format="json")
        cuerpo = r.json()
        self.assertIn("id", cuerpo)
        for campo in ("rut", "phone", "password", "password2"):
            self.assertNotIn(campo, cuerpo)

    def test_rechaza_rut_con_digito_invalido(self):
        r = self.client.post(self.url, payload(rut="12345678-9"), format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("rut", r.json())
        self.assertEqual(User.objects.count(), 0)

    def test_rechaza_correo_repetido_en_otras_mayusculas(self):
        self.client.post(self.url, payload(), format="json")
        r = self.client.post(self.url, payload(email="ANA@EXAMPLE.COM", rut="11111111-1",
                                               phone="+56987654321"), format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("email", r.json())

    def test_rechaza_telefono_mal_formado(self):
        r = self.client.post(self.url, payload(phone="912345678"), format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("phone", r.json())

    def test_rechaza_contrasenas_distintas(self):
        r = self.client.post(self.url, payload(password2="otra-clave-distinta"), format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("password2", r.json())

    def test_rechaza_contrasena_debil(self):
        r = self.client.post(self.url, payload(password="12345678", password2="12345678"),
                             format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("password", r.json())

    def test_la_clave_queda_con_argon2(self):
        self.client.post(self.url, payload(), format="json")
        self.assertTrue(User.objects.get().password.startswith("argon2$"))