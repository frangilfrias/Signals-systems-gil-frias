"""Tests para los servicios de generacion de senales (Milestone 1)."""

import numpy as np
import scipy.signal as signal

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

    def test_ruido_rosa(self):
        """Verifica que el espectro de la señal tenga una pendiente de aproximadamente -3 dB/octava"""
        # Generar ruido rosa con una duraciín mayor a 10 segundos con fs=44100 Hz
        duracion = 30
        fs = 44100
        ruido = generar_ruido_rosa(duracion, fs)
        # Calcular la PSD usando el método de Welch
        f, PSD = signal.welch(ruido, fs=fs, nperseg=4096)
        # Calcular la pendiente en dB/octava entre 100 Hz y 10.0 KHz
        mask = (f >= 100) & (f <= 10000)
        log2f = np.log2(f[mask])
        PSD_dB = 10 * np.log10(PSD[mask])
        # Verificar que la pendiente se encuentra entre -4.00 y -2.00 dB/octava
        pendiente, ordenada = np.polyfit(log2f, PSD_dB, 1)
        # print("Pendiente:", pendiente, "dB/octava")
        # Test solicitado
        assert -4 < pendiente < -2


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
