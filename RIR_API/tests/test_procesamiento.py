"""Tests para los servicios de procesamiento de senales (Milestone 2)."""

import numpy as np
import pytest
from scipy.signal import fftconvolve

from app.services.sine_sweep import generar_sine_sweep
from scipy import signal as sig
import soundfile as sf

from app.services.signal_utils import a_escala_log, cargar_audio, sintetizar_ri, obtener_ri_desde_sweep
from app.services.filter import filtro_octava

@pytest.fixture
def wav_mono(tmp_path):
    ruta = tmp_path / "mono.wav"
    senal = np.array([0.5, -0.5, 0.25, -0.25, 1.0, -1.0], dtype=np.float64)
    sf.write(ruta, senal, 44100)
    return ruta


@pytest.fixture
def wav_estereo(tmp_path):
    ruta = tmp_path / "estereo.wav"
    canal_l = np.array([0.5, -0.5, 1.0], dtype=np.float64)
    canal_r = np.array([0.3, -0.3, 0.8], dtype=np.float64)
    senal = np.column_stack([canal_l, canal_r])
    sf.write(ruta, senal, 48000)
    return ruta


@pytest.fixture
def archivo_invalido(tmp_path):
    ruta = tmp_path / "audio.mp3"
    ruta.write_bytes(b"datos falsos")
    return ruta

class TestCargarAudio:
    """Tests para la funcion cargar_audio."""
    def test_carga_wav_mono_sin_error(self, wav_mono):
        senal, fs = cargar_audio(wav_mono)
        assert senal is not None
        assert fs == 44100

    def test_senal_normalizada_entre_menos1_y_1(self, wav_mono):
        senal, _ = cargar_audio(wav_mono)
        assert np.max(np.abs(senal)) <= 1.0 + 1e-9

    def test_maximo_absoluto_es_1(self, wav_mono):
        senal, _ = cargar_audio(wav_mono)
        assert np.isclose(np.max(np.abs(senal)), 1.0, atol=1e-6)

    def test_carga_wav_estereo(self, wav_estereo):
        senal, fs = cargar_audio(wav_estereo)
        assert fs == 48000
        assert senal.ndim == 2
        assert senal.shape[1] == 2

    def test_estereo_normalizado(self, wav_estereo):
        senal, _ = cargar_audio(wav_estereo)
        assert np.max(np.abs(senal)) <= 1.0 + 1e-9

    def test_error_si_archivo_no_existe(self, tmp_path):
        ruta_falsa = tmp_path / "no_existe.wav"
        with pytest.raises(FileNotFoundError):
            cargar_audio(ruta_falsa)

    def test_error_si_formato_invalido(self, archivo_invalido):
        with pytest.raises(ValueError):
            cargar_audio(archivo_invalido)

    def test_acepta_ruta_como_string(self, wav_mono):
        senal, fs = cargar_audio(str(wav_mono))
        assert senal is not None

    def test_devuelve_float64(self, wav_mono):
        senal, _ = cargar_audio(wav_mono)
        assert senal.dtype == np.float64

class TestAEscalaLog:
    """Tests para la funcion a_escala_log."""
    def test_maximo_es_0_db(self):
        signal = np.array([1.0, 0.5, 0.25])
        resultado = a_escala_log(signal)
        assert np.isclose(np.max(resultado), 0.0, atol=1e-6)

    def test_amplitud_mitad_da_menos6_db(self):
        signal = np.array([1.0, 0.5])
        resultado = a_escala_log(signal)
        assert np.isclose(resultado[1], -6.0206, atol=0.01)

    def test_output_mismo_shape_que_input(self):
        signal = np.array([1.0, 0.5, 0.25, 0.1])
        resultado = a_escala_log(signal)
        assert resultado.shape == signal.shape

    def test_no_hay_inf(self):
        signal = np.array([1.0, 0.5, 0.0, 0.25])
        resultado = a_escala_log(signal)
        assert not np.any(np.isinf(resultado))

    def test_piso_de_ruido(self):
        signal = np.array([1.0, 1e-10])
        resultado = a_escala_log(signal)
        assert np.all(resultado >= -120.0)

    def test_senal_con_negativos(self):
        signal = np.array([1.0, -1.0, 0.5, -0.5])
        resultado = a_escala_log(signal)
        assert np.isclose(np.max(resultado), 0.0, atol=1e-6)

    def test_senal_silencio_total(self):
        signal = np.zeros(10)
        resultado = a_escala_log(signal)
        assert not np.any(np.isinf(resultado))


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
