from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.accounts.validators import normalize_rut, rut_check_digit, validate_rut


class RutTests(SimpleTestCase):
    def test_calcula_el_digito_verificador(self):
        self.assertEqual(rut_check_digit("11111111"), "1")
        self.assertEqual(rut_check_digit("12345678"), "5")
        self.assertEqual(rut_check_digit("10000004"), "0")
        self.assertEqual(rut_check_digit("10000013"), "K")

    def test_normaliza_los_formatos_habituales(self):
        self.assertEqual(normalize_rut("12.345.678-5"), "12345678-5")
        self.assertEqual(normalize_rut(" 12345678-5 "), "12345678-5")
        self.assertEqual(normalize_rut("123456785"), "12345678-5")
        self.assertEqual(normalize_rut("10.000.013-k"), "10000013-K")

    def test_acepta_ruts_validos(self):
        for rut in ("11111111-1", "12.345.678-5", "10000004-0", "10000013-K"):
            validate_rut(rut)

    def test_rechaza_digito_verificador_incorrecto(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_rut("12345678-9")
        self.assertEqual(ctx.exception.code, "rut_dv")

    def test_rechaza_formatos_invalidos(self):
        casos = ["", "abc", "1234-5", "123456789012-3", "12345678-", "12345678-5\n",
                 "１２３４５６７８-５", "12345678-5; DROP TABLE", "12 345 678-5 x"]
        for rut in casos:
            with self.subTest(rut=rut):
                with self.assertRaises(ValidationError):
                    validate_rut(rut)