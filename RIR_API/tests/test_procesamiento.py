"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest

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
        fs = 44100
        fc = 1000
        duracion = 4

        t = np.arange(0, duracion, 1 / fs)

        # senal senoidal de igual frecuencia a la frecuencia central
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

        # Comprobación de la tolerancia +/- 1 dB
        assert abs(ganancia_db) <= 1.0

    def test_filtro_octava_atenuacion(self):
        """Verificar atenuacion fuera de la banda de paso."""
        fs = 44100
        fc = 1000
        orden = 4
        duracion = 2.0

        t = np.arange(0, duracion, 1 / fs)

        # Señal 1: por debajo de la frecuencia de corte inferior
        f_baja = fc / 2
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

        # Señal 2: por encima de la frecuencia de corte superior
        f_alta = fc * 2
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

        # comprobación
        assert ganancia_db_low < -20
        assert ganancia_db_high < -20

    def test_filtro_octava_respuesta_frecuencia(self):
        """Verificar que la respuesta cumple -3 dB en frecuencias de corte."""
        fs = 48000
        fc = 1000
        orden = 4

        # Frecuencias de corte
        f_low = fc / np.sqrt(2)
        f_high = fc * np.sqrt(2)

        duracion = 2.0
        t = np.arange(0, duracion, 1 / fs)

        for frecuencia in (f_low, f_high):
            # Señal senoidal de amplitud unitaria
            signal = np.sin(2 * np.pi * frecuencia * t)

            # Aplicar la función bajo prueba
            signal_filtrada = filtro_octava(
                signal=signal,
                fc=fc,
                fs=fs,
                orden=orden,
            )

            # Eliminar transitorios de borde
            inicio = len(signal) // 4
            fin = 3 * len(signal) // 4

            signal_util = signal[inicio:fin]
            filtrada_util = signal_filtrada[inicio:fin]

            # Amplitudes RMS convertidas a amplitud pico
            amp_entrada = np.sqrt(2 * np.mean(signal_util**2))

            amp_salida = np.sqrt(2 * np.mean(filtrada_util**2))

            ganancia_db = 20 * np.log10(amp_salida / amp_entrada)

            # Al ser un filtro forward-backward (sosfiltfilt), la ganancia en las frecuencias de
            # corte es -6.00 dB
            assert np.isclose(
                ganancia_db,
                -6.0,
                atol=0.5,
            ), f"Ganancia en {frecuencia:.1f} Hz = {ganancia_db:.2f} dB"
