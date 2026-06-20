import numpy as np
import pytest
import soundfile as sf

from app.services.signal_utils import cargar_audio


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
