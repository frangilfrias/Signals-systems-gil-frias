"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest

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

    import numpy as np


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

    # tolerancia del 20 %
    assert abs(t60_estimado - t60_objetivo) < 0.1 * t60_objetivo
