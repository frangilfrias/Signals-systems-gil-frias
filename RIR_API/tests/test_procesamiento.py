"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest
from scipy.signal import fftconvolve

from app.services.signal_utils import a_escala_log, cargar_audio
from app.services.sine_sweep import generar_sine_sweep
from app.services.signal_utils import obtener_ri_desde_sweep

class TestCargarAudio:
    """Tests para la funcion cargar_audio."""

    def test_cargar_audio_no_existe(self):
        """Verifica que se lanza FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            cargar_audio("archivo_que_no_existe.wav")

    def test_cargar_audio_retorna_tupla(self):
        """Verifica que retorna una tupla (signal, fs) — requiere archivo de prueba."""
        pytest.skip("Requiere archivo de audio de prueba")


class TestAEscalaLog:
    """Tests para la funcion a_escala_log."""

    def test_a_escala_log_valores(self):
        """Verifica que el maximo de la senal corresponde a 0 dB."""
        x = np.array([1.0, 0.5, 0.25, 0.1])
        db = a_escala_log(x)
        assert abs(db[0] - 0.0) < 1e-10

    def test_a_escala_log_tipo(self):
        """Verifica que retorna un np.ndarray."""
        x = np.array([1.0, 0.5])
        db = a_escala_log(x)
        assert isinstance(db, np.ndarray)

class TestObtenerRiDesdeSweep:
    def test_obtener_ri_pico(self):
        """
        Verificar que la RI obtenida por deconvolucion tiene
        un pico principal claramente identificable.
        """

        fs = 48000

        # Sweep + filtro de prueba
        sweep, filtro_inverso = generar_sine_sweep(
            f1=20,
            f2=20000,
            duracion=2.0,
            fs=fs,
        )

        # RI artificial simple, con reflexiones
        ri_original = np.zeros(2048)
        ri_original[0] = 1.0
        ri_original[300] = 0.5
        ri_original[700] = 0.25

        # Simular grabacion
        grabacion = fftconvolve(
            sweep,
            ri_original,
            mode="full",
        )

        # Recuperar RI
        ri_recuperada = obtener_ri_desde_sweep(
            grabacion,
            filtro_inverso,
        )

        # Re-alineo las señales utilizando el pico como referencia
        idx = np.argmax(np.abs(ri_recuperada))
        ri_recuperada = ri_recuperada[idx:]

        # Igualar longitudes para comparar
        n = min(len(ri_original), len(ri_recuperada))

        ri_original = ri_original[:n]
        ri_recuperada = ri_recuperada[:n]

        # Correlacion normalizada
        correlacion = np.corrcoef(
            ri_original,
            ri_recuperada,
        )[0, 1]

        assert correlacion > 0.9
