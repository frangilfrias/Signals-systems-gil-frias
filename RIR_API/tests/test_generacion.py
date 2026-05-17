"""Tests para los servicios de generacion de senales (Milestone 1)."""

import numpy as np
import pytest
from scipy.signal import spectrogram
from scipy.signal import fftconvolve

from app.services.pink_noise import generar_ruido_rosa
from app.services.sine_sweep import generar_sine_sweep


class TestGenerarRuidoRosa:
    """Tests para la funcion generar_ruido_rosa."""

    def test_ruido_rosa_duracion(self):
        """Verifica que la longitud de la senal corresponda a duracion * fs."""
        duracion = 2.0
        fs = 44100
        ruido = generar_ruido_rosa(duracion, fs)
        expected_length = int(duracion * fs)
        assert len(ruido) == expected_length

    def test_ruido_rosa_tipo(self):
        """Verifica que la funcion retorna un np.ndarray."""
        ruido = generar_ruido_rosa(1.0, 44100)
        assert isinstance(ruido, np.ndarray)

    def test_ruido_rosa_normalizado(self):
        """Verifica que la senal esta normalizada entre -1 y 1."""
        ruido = generar_ruido_rosa(1.0, 44100)
        assert np.max(np.abs(ruido)) <= 1.0


class TestGenerarSineSweep:
    """Tests para la funcion generar_sine_sweep."""

    def test_sine_sweep_retorna_tupla(self):
        """Verifica que retorna una tupla con dos arrays."""
        resultado = generar_sine_sweep(20, 20000, 1.0, 44100)
        assert isinstance(resultado, tuple)
        assert len(resultado) == 2
        assert isinstance(resultado[0], np.ndarray)
        assert isinstance(resultado[1], np.ndarray)

    def test_sine_sweep_duracion(self):
        """Verifica que ambas senales tienen la longitud correcta."""
        duracion = 3.0
        fs = 44100
        sweep, filtro_inv = generar_sine_sweep(20, 20000, duracion, fs)
        expected_length = int(duracion * fs)
        assert len(sweep) == expected_length
        assert len(filtro_inv) == expected_length

    def test_sine_sweep_rango_frecuencias(self):
        """
        Verificar que el sine sweep cubre el rango de frecuencias
        especificado de f1 a f2 de manera correcta.
        """
        sweep, filtroinv = generar_sine_sweep(20, 20000, 5.0, 44100)
        frecuencias, tiempos, Sxx = spectrogram(sweep,fs=44100)

        ### Analizo si hay energia significativa en las frecuencias inicial y final
        #Busco los indices  en los 20 y 20000Hz
        idx_f1 = np.argmin(np.abs(frecuencias - 20))
        idx_f2 = np.argmin(np.abs(frecuencias - 20000))

        #Mido la energía de dichos puntos
        energia_f1 = np.max(Sxx[idx_f1])
        energia_f2 = np.max(Sxx[idx_f2])

        assert energia_f1 > 1e-10, ("No se detectó energía significativa cerca de la frecuencia inicial (20 Hz)")
        assert energia_f2 > 1e-10, ("No se detectó energía significativa cerca de la frecuencia final (20000 Hz)")

        ### Analizo si el crecimiento de la frecuencia instantanea es monotona
        #Busco frecuencia con mayor energia
        indices_maximos = np.argmax(Sxx, axis=0)
        frecuencia_inst = frecuencias[indices_maximos]

        #Verifico que vaya creciendo con una tolerancia de 5 Hz
        diferencias = np.diff(frecuencia_inst)
        porcentaje_creciente = np.mean(diferencias >= 0)

        assert porcentaje_creciente > 0.9, ("La frecuencia instantánea no presenta crecimiento monotónico suficiente")

    def test_sine_sweep_convolucion_impulso(self):
        """
        Verificar que la convolucion del sweep con su filtro inverso
        produce una aproximacion a un impulso.
        """
        #Genero la señal, el filtro y hago la convolucion
        sweep, filtro = generar_sine_sweep(20, 20000, 1.0, 44100)
        respuesta = fftconvolve(sweep, filtro,mode = "full")

        #Busco la posicion del pico maximo 
        idx_pico = np.argmax(np.abs(respuesta))
        pico = np.abs(respuesta[idx_pico])

        #Excluyo la ventana
        ventana = 100
        resto = np.concatenate([
            respuesta[:idx_pico - ventana],
            respuesta[idx_pico + ventana:]
            ])

        #Mido la energia promedio del resto
        energia_promedio_resto = np.mean(np.abs(resto))

        #Comparo el pico con el resto
        relacion_db = 20 * np.log10(
            pico / energia_promedio_resto
        )

        assert relacion_db > 40, ("La relación pico/resto es insuficiente: ")