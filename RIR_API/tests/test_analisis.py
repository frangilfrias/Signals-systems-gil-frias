"""Tests para los servicios de analisis de parametros acusticos (Milestone 3)."""

import numpy as np

from app.services.acoustic_parameters import integral_schroeder, regresion_lineal, suavizar_signal


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


class TestSuavizarSenal:
    """Tests para la función suavizar_signal."""

    def test_suavizar_hilbert_envolvente(self):
        """
        La envolvente obtenida mediante Hilbert debe ser no negativa.
        """
        fs = 1000

        # Señal senoidal modulada en amplitud
        t = np.arange(fs) / fs
        signal = (1 + 0.5 * np.sin(2 * np.pi * 2 * t)) * np.sin(
            2 * np.pi * 50 * t,
        )

        envolvente = suavizar_signal(signal, "hilbert")

        # La envolvente es el módulo de una señal compleja,
        # por lo que nunca debe ser negativa.
        assert np.all(envolvente >= 0)

        # La longitud debe preservarse.
        assert envolvente.shape == signal.shape

    def test_suavizar_media_movil_longitud(self):
        """
        La salida de la media móvil debe tener
        la misma longitud que la entrada.
        """
        signal = np.random.randn(48000)

        suavizada = suavizar_signal(signal, 100)

        assert suavizada.shape == signal.shape
