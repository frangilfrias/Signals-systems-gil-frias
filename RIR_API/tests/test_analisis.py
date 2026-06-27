"""Tests para los servicios de analisis de parametros acusticos (Milestone 3)."""

import numpy as np
import pytest

from app.services.acoustic_parameters import (
    integral_schroeder,
    regresion_lineal,
    calcular_parametros_acusticos
)
from app.services.signal_utils import sintetizar_ri


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


class TestCalcularParametrosAcusticos:
    """Tests para la función calcular_parametros_acusticos."""

    def test_parametros_ri_sintetizada(self):
        """Verifica que el T30 estimado sea cercano (+-10%)
        al T60 sintetizado."""

        fs = 48000
        t60 = 2.0

        # Evitar fallos debido a la variabilidad del ruido aleatorio
        np.random.seed(0)

        ri = sintetizar_ri(
            {1000: t60},
            fs=fs,
            duracion=5.0,
        )

        parametros = calcular_parametros_acusticos(
            ri,
            fs,
        )

        t30 = parametros["T30"][1000]

        assert np.isclose(
            t30,
            t60,
            rtol=0.10,
        )

    def test_d50_rango(self):
        """D50 debe pertenecer al intervalo 0% y 100%."""

        fs = 48000

        # Evita fallos debido a la variabilidad del ruido aleatorio
        np.random.seed(0)

        ri = sintetizar_ri(
            {1000: 2.0},
            fs=fs,
            duracion=5.0,
        )

        parametros = calcular_parametros_acusticos(
            ri,
            fs,
        )

        d50 = parametros["D50"][1000]

        assert 0 <= d50 <= 100

    def test_c80_consistencia(self):
        """Una RI con energía concentrada al comienzo debe tener C80>0."""

        fs = 48000

        # Evita fallos debido a la variabilidad del ruido aleatorio
        np.random.seed(0)

        ri = np.zeros(fs)

        ri[0] = 1

        parametros = calcular_parametros_acusticos(
            ri,
            fs,
        )

        c80 = parametros["C80"][125]

        assert c80 > 0
