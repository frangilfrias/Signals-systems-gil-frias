"""Tests para los servicios de analisis de parametros acusticos (M 3)."""

import numpy as np
import pytest

from app.services.acoustic_parameters import (
    calcular_parametros_acusticos,
    integral_schroeder,
    metodo_lundeby,
    regresion_lineal,
    suavizar_signal,
)
from app.services.signal_utils import sintetizar_ri


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


class TestMetodoLundeby:
    """Tests para la función metodo_lundeby"""

    def test_lundeby_basico(self):
        fs = 48000

        # RI simple exponencial + ruido pequeño
        t = np.arange(fs) / fs
        ri = np.exp(-3 * t)

        idx, ruido = metodo_lundeby(ri, fs)

        # debe estar dentro de la señal
        assert 0 <= idx < len(ri)
        assert isinstance(ruido, float)

    def test_lundeby_ruido_valido(self):
        fs = 48000

        ri = np.zeros(fs)
        ri[0] = 1
        ri += 0.001 * np.random.randn(fs)

        idx, ruido = metodo_lundeby(ri, fs)

        assert isinstance(idx, int)
        assert isinstance(ruido, float)

    def test_lundeby_sin_senal(self):
        fs = 48000

        ri = 0.0001 * np.random.randn(fs)

        idx, ruido = metodo_lundeby(ri, fs)

        # debería devolver algo válido (no romperse)
        assert isinstance(idx, int)
        assert isinstance(ruido, float)
        assert 0 <= idx < len(ri)

    def test_lundeby_estabilidad(self):
        fs = 48000

        np.random.seed(0)
        ri1 = np.random.randn(fs) * np.exp(-3 * np.arange(fs) / fs)

        np.random.seed(0)
        ri2 = np.random.randn(fs) * np.exp(-3 * np.arange(fs) / fs)

        idx1, _ = metodo_lundeby(ri1, fs)
        idx2, _ = metodo_lundeby(ri2, fs)

        assert abs(idx1 - idx2) < 10
