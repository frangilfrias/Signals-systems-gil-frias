"""Tests para los servicios de analisis de parametros acusticos (Milestone 3)."""

import numpy as np

from app.services.acoustic_parameters import integral_schroeder, regresion_lineal


class TestRegresionLineal:
    """Tests para la funcion regresion_lineal."""

    def test_regresion_lineal_conocida(self):
        """Verifica con una recta conocida y = 2x + 1."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        y = 2.0 * x + 1.0
        pendiente, ordenada = regresion_lineal(x, y)
        assert abs(pendiente - 2.0) < 1e-10
        assert abs(ordenada - 1.0) < 1e-10

    def test_regresion_lineal_con_ruido(self):
        """Verifica que la regresion se aproxima a la recta con datos ruidosos."""
        np.random.seed(42)
        x = np.linspace(0, 10, 100)
        y = 3.0 * x + 5.0 + np.random.normal(0, 0.1, 100)
        pendiente, ordenada = regresion_lineal(x, y)
        assert abs(pendiente - 3.0) < 0.5
        assert abs(ordenada - 5.0) < 1.0


class TestIntegralSchroeder:
    """Tests para la funcion integral_schroeder."""

    def test_integral_schroeder_forma(self):
        """Verifica que la EDC tiene la misma longitud que la entrada."""
        ri = np.random.randn(1000)
        edc = integral_schroeder(ri)
        assert len(edc) == len(ri)

    def test_integral_schroeder_decreciente(self):
        """Verifica que la EDC es monotonamente decreciente."""
        ri = np.random.randn(1000)
        edc = integral_schroeder(ri)
        assert np.all(np.diff(edc) <= 0)

    import numpy as np


class TestIntegralSchroeder:
    """Tests para la función integral_schroeder."""

    def test_schroeder_ri_sintetizada(self):
        """
        Para una RI sintetizada con T60 conocido,
        la curva de Schroeder debe ser aproximadamente lineal
        con pendiente -60/T60 dB/s.
        """
        fs = 48000
        t60 = 1.5  # s

        # Duración suficiente para observar el decaimiento
        duracion = 3 * t60
        t = np.arange(int(fs * duracion)) / fs

        # RI exponencial:
        # amplitud ~ exp(-a t)
        # energía ~ exp(-2 a t)
        a = 3 * np.log(10) / t60
        ri = np.exp(-a * t)

        # EDC normalizada
        edc = integral_schroeder(ri)

        # Conversión a dB
        edc_db = 10 * np.log10(np.maximum(edc, np.finfo(float).eps))

        # Ajuste lineal sobre la zona útil
        mascara = (edc_db < -5) & (edc_db > -35)

        pendiente, _ = np.polyfit(
            t[mascara],
            edc_db[mascara],
            deg=1,
        )

        pendiente_esperada = -60 / t60

        assert np.isclose(
            pendiente,
            pendiente_esperada,
            rtol=0.05,
        )

    def test_schroeder_maximo_cero_db(self):
        """El primer valor de la integral de Schroeder debe ser 0 dB."""

        ri = np.array([1.0, 0.5, 0.25])

        edc = integral_schroeder(ri)

        edc_db = 10 * np.log10(np.maximum(edc, np.finfo(float).eps))

        assert np.isclose(
            edc_db[0],
            0.0,
            atol=1e-12,
        )
