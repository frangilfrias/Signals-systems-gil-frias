"""Tests para los servicios de analisis de parametros acusticos (Milestone 3)."""

import numpy as np
import pytest

from app.services.acoustic_parameters import (
    integral_schroeder,
    regresion_lineal,
    metodo_lundeby
)


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

class TestMetodoLundeby:
    """Tests para la función metodo_lundeby"""
    def test_lundeby_basico(self):
        fs = 48000

        # RI simple exponencial + ruido pequeño
        t = np.arange(fs) / fs
        ri = np.exp(-3 * t)

        idx = metodo_lundeby(ri, fs)

        # debe estar dentro de la señal
        assert 0 < idx < len(ri)

    def test_lundeby_ruido_valido(self):
        fs = 48000

        ri = np.zeros(fs)
        ri[0] = 1
        ri += 0.001 * np.random.randn(fs)

        idx = metodo_lundeby(ri, fs)

        assert isinstance(idx, int)
        assert 0 <= idx < len(ri)

    def test_lundeby_sin_senal(self):
        fs = 48000

        ri = 0.0001 * np.random.randn(fs)

        idx = metodo_lundeby(ri, fs)

        # debería devolver algo válido (no romperse)
        assert isinstance(idx, int)
        assert 0 <= idx < len(ri)

    def test_lundeby_estabilidad(self):
        fs = 48000

        np.random.seed(0)
        ri1 = np.random.randn(fs) * np.exp(-3*np.arange(fs)/fs)

        np.random.seed(0)
        ri2 = np.random.randn(fs) * np.exp(-3*np.arange(fs)/fs)

        idx1 = metodo_lundeby(ri1, fs)
        idx2 = metodo_lundeby(ri2, fs)

        assert abs(idx1 - idx2) < 10
