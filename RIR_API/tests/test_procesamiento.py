"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest
from scipy import signal as sig

from app.services.filter import filtro_octava
from app.services.signal_utils import a_escala_log, cargar_audio


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


class TestFiltroOctava:
    """Tests para la funcion filtro_octava."""

    def test_filtro_octava_frecuencia_central(self):
        """Verificar que el filtro pasa correctamente la frecuencia central."""
        fs = 44000
        fc = 1000
        duracion = 4

        t = np.arange(0, duracion, 1 / fs)

        # senoide exactamente en la frecuencia central
        x = np.sin(2 * np.pi * fc * t)

        y = filtro_octava(
            signal=x,
            fc=fc,
            fs=fs,
            orden=4,
        )

        rms_entrada = np.sqrt(np.mean(x**2))
        rms_salida = np.sqrt(np.mean(y**2))

        ganancia_db = 20 * np.log10(rms_salida / rms_entrada)

        assert ganancia_db > -1.0

    def test_filtro_octava_atenuacion(self):
        """Verificar atenuacion fuera de banda."""
        fs = 44000
        fc = 16000
        orden = 4
        duracion = 2.0

        t = np.arange(0, duracion, 1 / fs)

        # -----------------------------
        # Señal 1: fuera de banda baja
        # -----------------------------
        f_baja = fc / 4
        x_low = np.sin(2 * np.pi * f_baja * t)

        y_low = filtro_octava(
            signal=x_low,
            fc=fc,
            fs=fs,
            orden=orden,
        )

        rms_in_low = np.sqrt(np.mean(x_low**2))
        rms_out_low = np.sqrt(np.mean(y_low**2))
        ganancia_db_low = 20 * np.log10(rms_out_low / rms_in_low)

        # -----------------------------
        # Señal 2: fuera de banda alta
        # -----------------------------
        f_alta = fc * 4
        x_high = np.sin(2 * np.pi * f_alta * t)

        y_high = filtro_octava(
            signal=x_high,
            fc=fc,
            fs=fs,
            orden=orden,
        )

        rms_in_high = np.sqrt(np.mean(x_high**2))
        rms_out_high = np.sqrt(np.mean(y_high**2))
        ganancia_db_high = 20 * np.log10(rms_out_high / rms_in_high)

        # -----------------------------
        # Criterio robusto
        # -----------------------------
        assert ganancia_db_low < -20
        assert ganancia_db_high < -20

    def test_filtro_octava_respuesta_frecuencia(self):
        """Verificar que la respuesta cumple -3 dB en frecuencias de corte."""
        fs = 44100
        fc = 16000
        orden = 4

        # ejecutar filtro (sin reconstruir nada)
        sos = filtro_octava(
            signal=np.zeros(1000),
            fc=fc,
            fs=fs,
            orden=orden,
        )

        # frecuencias de corte del diseño
        f_low = fc / np.sqrt(2)
        f_high = fc * np.sqrt(2)

        # respuesta en frecuencia del MISMO filtro
        w, h = sig.sosfreqz(sos, worN=4096, fs=fs)

        h_db = 20 * np.log10(np.abs(h) + 1e-12)

        h_low = np.interp(f_low, w, h_db)
        h_high = np.interp(f_high, w, h_db)

        assert np.isclose(h_low, -3, atol=1.5), f"f_low={h_low:.2f} dB"
        assert np.isclose(h_high, -3, atol=1.5), f"f_high={h_high:.2f} dB"
