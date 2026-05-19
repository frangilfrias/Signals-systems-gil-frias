from unittest.mock import patch

import numpy as np
import pytest

from app.services.reproducir_grabar import reproducir_y_grabar

fs = 44100
duracion = 2.0
duracion_grabacion = 3.0

t = np.linspace(0, duracion, int(duracion * fs), endpoint=False)
signal_mono = 0.5 * np.sin(2 * np.pi * 440 * t)
signal_stereo = np.column_stack((signal_mono, signal_mono))


# Test 1: ejecución correcta (mono)


@patch("sounddevice.playrec")
@patch("sounddevice.wait")
@patch("sounddevice.query_devices")
def test_rec_play_mono(mock_query, mock_wait, mock_playrec):
    mock_query.return_value = True

    frames = int(duracion_grabacion * fs)
    mock_playrec.return_value = np.zeros((frames, 1))

    grabacion = reproducir_y_grabar(signal_mono, fs, duracion_grabacion)

    assert isinstance(grabacion, np.ndarray)
    assert grabacion.shape[0] == frames
    assert grabacion.shape[1] == 1


# Test 2: ejecución correcta (estéreo)


@patch("sounddevice.playrec")
@patch("sounddevice.wait")
@patch("sounddevice.query_devices")
def test_rec_play_stereo(mock_query, mock_wait, mock_playrec):
    mock_query.return_value = True

    frames = int(duracion_grabacion * fs)
    mock_playrec.return_value = np.zeros((frames, 2))

    grabacion = reproducir_y_grabar(signal_stereo, fs, duracion_grabacion)

    assert isinstance(grabacion, np.ndarray)
    assert grabacion.shape[1] == 2


# Test 3: duración insuficiente


@patch("sounddevice.query_devices")
def test_duracion_insuficiente(mock_query):
    mock_query.return_value = True

    duracion_corta = 1.0  # menor que la señal

    with pytest.raises(ValueError):
        reproducir_y_grabar(signal_mono, fs, duracion_corta)


# Test 4: error de dispositivos


@patch("sounddevice.query_devices")
def test_error_dispositivo(mock_query):
    mock_query.side_effect = Exception("No device")

    with pytest.raises(RuntimeError):
        reproducir_y_grabar(signal_mono, fs, duracion_grabacion)


# Test 5: verificación de llamada a playrec


@patch("sounddevice.playrec")
@patch("sounddevice.wait")
@patch("sounddevice.query_devices")
def test_playrec_llamado_correctamente(mock_query, mock_wait, mock_playrec):
    mock_query.return_value = True

    frames = int(duracion_grabacion * fs)
    mock_playrec.return_value = np.zeros((frames, 1))

    reproducir_y_grabar(signal_mono, fs, duracion_grabacion)

    mock_playrec.assert_called_once()

    args, kwargs = mock_playrec.call_args

    # kwargs esperados
    assert kwargs["samplerate"] == fs
    assert kwargs["channels"] == 1


# Test 6: tipo de salida consistente


@patch("sounddevice.playrec")
@patch("sounddevice.wait")
@patch("sounddevice.query_devices")
def test_tipo_salida(mock_query, mock_wait, mock_playrec):
    mock_query.return_value = True

    frames = int(duracion_grabacion * fs)
    mock_playrec.return_value = np.zeros((frames, 1))

    grabacion = reproducir_y_grabar(signal_mono, fs, duracion_grabacion)

    assert grabacion.dtype == np.float64 or grabacion.dtype == np.float32
