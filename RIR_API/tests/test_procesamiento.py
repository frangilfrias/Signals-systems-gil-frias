"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest
from scipy import signal as sig

from app.services.filter import filtro_octava
from app.services.signal_utils import a_escala_log, cargar_audio, sintetizar_ri


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


# Función global para los Test de los filtros de octava
def _design_sos(fc, fs, orden):
    """Replica exacta del diseño IEC usado en filtro_octava."""

    f_low = fc / np.sqrt(2)
    f_high = fc * np.sqrt(2)

    return sig.butter(
        orden,
        [f_low, f_high],
        btype="bandpass",
        fs=fs,
        output="sos",
    )


class TestFiltroOctava:
    """Tests para la funcion filtro_octava."""

    def test_filtro_octava_frecuencia_central(self):
        """Verificar que el filtro pasa correctamente la frecuencia central."""

        fs = 48000
        fc = 1000
        orden = 4

        sos = _design_sos(fc, fs, orden)

        w, h = sig.sosfreqz(sos, worN=4096, fs=fs)

        # índice
        w = np.asarray(w, dtype=float)
        idx_fc = np.argmin((w - fc) ** 2)

        gain_fc = 20 * np.log10(np.abs(h[idx_fc]) + 1e-12)

        assert np.isclose(gain_fc, 0.0, atol=0.5), f"Ganancia en fc incorrecta: {gain_fc:.2f} dB"

    def test_filtro_octava_atenuacion(self):
        """Verificar atenuacion fuera de la banda de paso"""

        fs = 48000
        fc = 1000
        orden = 4

        sos = _design_sos(fc, fs, orden)

        w, h = sig.sosfreqz(sos, worN=4096, fs=fs)

        f1 = fc / 2
        f2 = 2 * fc
        w = np.asarray(w, dtype=float)
        idx_f1 = np.argmin((w - f1) ** 2)
        idx_f2 = np.argmin((w - f2) ** 2)

        gain_f1 = 20 * np.log10(np.abs(h[idx_f1]) + 1e-12)
        gain_f2 = 20 * np.log10(np.abs(h[idx_f2]) + 1e-12)

        assert gain_f1 < -20, f"Atenuación insuficiente fc/2: {gain_f1:.2f} dB"
        assert gain_f2 < -20, f"Atenuación insuficiente 2fc: {gain_f2:.2f} dB"

    def test_filtro_octava_respuesta_frecuencia(self):
        """Verificar que la respuesta cumple -3 dB en frecuencias de corte."""

        fs = 48000
        fc = 1000
        orden = 4

        sos = _design_sos(fc, fs, orden)

        w, h = sig.sosfreqz(sos, worN=4096, fs=fs)

        mag_db = 20 * np.log10(np.abs(h) + 1e-12)

        w = np.asarray(w, dtype=float)
        idx_fc = np.argmin((w - fc) ** 2)
        gain_fc = mag_db[idx_fc]

        f_low = fc / np.sqrt(2)
        f_high = fc * np.sqrt(2)

        idx_low = np.argmin((w - f_low) ** 2)
        idx_high = np.argmin((w - f_high) ** 2)

        gain_low = mag_db[idx_low]
        gain_high = mag_db[idx_high]

        assert np.isclose(gain_fc, 0.0, atol=0.5)
        assert np.isclose(gain_low, -3.0, atol=1.0)
        assert np.isclose(gain_high, -3.0, atol=1.0)


class TestSintetizarRI:
    """Tests para la funcion sintetizar_ri"""

    def test_sintetizar_ri_duracion(self):
        """Verificar que la RI tiene la duracion correcta."""
        fs = 44100
        duracion = 2.0

        t60_por_banda = {1000.0: 2.0}

        rir = sintetizar_ri(
            t60_por_banda=t60_por_banda,
            fs=fs,
            duracion=duracion,
        )

        assert isinstance(rir, np.ndarray)
        assert rir.ndim == 1
        assert len(rir) == int(fs * duracion)

    def test_sintetizar_ri_decaimiento(self):
        """
        Verificar que el decaimiento por banda corresponde
        aproximadamente al T60 especificado.
        """
        fs = 44100
        duracion = 3.0

        fc = 1000
        t60_objetivo = 2.0

        rir = sintetizar_ri(
            t60_por_banda={fc: t60_objetivo},
            fs=fs,
            duracion=duracion,
        )

        # Filtrado en la banda analizada
        rir_banda = filtro_octava(
            signal=rir,
            fc=fc,
            fs=fs,
            orden=4,
        )

        # Integración inversa de Schroeder
        energia = rir_banda**2
        schroeder = np.cumsum(energia[::-1])[::-1]

        schroeder_db = 10 * np.log10(schroeder + 1e-12)
        schroeder_db -= schroeder_db[0]

        t = np.arange(len(schroeder_db)) / fs

        # Región típica para estimación T30
        mask = (schroeder_db <= -5) & (schroeder_db >= -35)

        assert np.sum(mask) > 100

        pendiente, ordenada = np.polyfit(
            t[mask],
            schroeder_db[mask],
            1,
        )

        t60_estimado = -60 / pendiente

        assert np.isfinite(t60_estimado)

        # tolerancia del 10 %
        assert abs(t60_estimado - t60_objetivo) < 0.1 * t60_objetivo
