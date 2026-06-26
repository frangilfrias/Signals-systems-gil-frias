"""Tests para los servicios de analisis de parametros acusticos (Milestone 3)."""

import numpy as np

from app.services.acoustic_parameters import integral_schroeder, regresion_lineal, suavizar_signal


class TestRegresionLineal:
    def test_recta_perfecta(self):
        """Con datos perfectamente lineales R² debe ser 1.0."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        y = -10.0 * x + 5.0
        m, b, r2 = regresion_lineal(x, y)
        assert np.isclose(m, -10.0, atol=1e-6)
        assert np.isclose(b, 5.0, atol=1e-6)
        assert np.isclose(r2, 1.0, atol=1e-6)

    def test_pendiente_negativa(self):
        """La pendiente debe ser negativa en un decaimiento acustico."""
        x = np.linspace(0, 1, 100)
        y = -60.0 * x + 0.0
        m, b, r2 = regresion_lineal(x, y)
        assert m < 0

    def test_calculo_t60_desde_pendiente(self):
        """T60 = -60 / m debe dar el valor esperado."""
        x = np.linspace(0, 2, 200)
        y = -30.0 * x
        m, b, r2 = regresion_lineal(x, y)
        t60 = -60.0 / m
        assert np.isclose(t60, 2.0, atol=1e-4)

    def test_r_cuadrado_entre_0_y_1(self):
        """R² siempre debe estar entre 0 y 1."""
        rng = np.random.default_rng(42)
        x = np.linspace(0, 1, 50)
        y = -20.0 * x + rng.normal(0, 0.5, 50)
        m, b, r2 = regresion_lineal(x, y)
        assert 0.0 <= r2 <= 1.0

    def test_r_cuadrado_alto_con_poco_ruido(self):
        """Con poco ruido R² debe ser mayor a 0.99."""
        rng = np.random.default_rng(0)
        x = np.linspace(0, 1, 100)
        y = -30.0 * x + rng.normal(0, 0.01, 100)
        m, b, r2 = regresion_lineal(x, y)
        assert r2 > 0.99

    def test_devuelve_tres_floats(self):
        """Debe devolver una tupla de tres floats."""
        x = np.array([0.0, 1.0, 2.0])
        y = np.array([0.0, -10.0, -20.0])
        resultado = regresion_lineal(x, y)
        assert len(resultado) == 3
        assert all(isinstance(v, float) for v in resultado)

    def test_error_arrays_distinto_largo(self):
        """Debe lanzar ValueError si x e y tienen distinto largo."""
        x = np.array([0.0, 1.0, 2.0])
        y = np.array([0.0, -10.0])
        with pytest.raises(ValueError):
            regresion_lineal(x, y)

    def test_error_menos_de_2_puntos(self):
        """Debe lanzar ValueError si hay menos de 2 puntos."""
        x = np.array([0.0])
        y = np.array([-5.0])
        with pytest.raises(ValueError):
            regresion_lineal(x, y)

    def test_error_x_constante(self):
        """Debe lanzar ValueError si todos los x son iguales."""
        x = np.array([1.0, 1.0, 1.0])
        y = np.array([0.0, -10.0, -20.0])
        with pytest.raises(ValueError):
            regresion_lineal(x, y)

    def test_acepta_arrays_de_enteros(self):
        """Debe funcionar aunque los arrays entren como int."""
        x = np.array([0, 1, 2, 3])
        y = np.array([0, -10, -20, -30])
        m, b, r2 = regresion_lineal(x, y)
        assert np.isclose(m, -10.0, atol=1e-6)


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


class TestSuavizarSignal:
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
